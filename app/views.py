import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Message

main_bp = Blueprint('main', __name__)

def maybe_dev_login():
    """If DEV_AUTH_BYPASS is enabled, allow setting a dev user via header or query param.
    This is strictly for local development/testing. It creates the user if missing and logs them in.
    """
    try:
        if not current_app.config.get('DEV_AUTH_BYPASS'):
            return
    except RuntimeError:
        # current_app not available at import time
        return

    dev_user = request.headers.get('X-DEV-USER') or request.args.get('_dev_user')
    if not dev_user:
        return

    user = User.query.filter_by(email=dev_user).first()
    if not user:
        user = User(email=dev_user, password=generate_password_hash('devpass'))
        db.session.add(user)
        db.session.commit()
    login_user(user)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json or request.form
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify({'message': 'ok'})
    return render_template('signup.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json or request.form
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        login_user(user)
        return jsonify({'message': 'ok'})
    return render_template('login.html')


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


def generate_ai_response(prompt, history=None):
    """Generate response by calling the LLM service (llm_service.py).
    
    Requires LLM_SERVICE_URL environment variable pointing to the service (e.g., http://127.0.0.1:5001).
    Falls back to a helpful canned response if service is unreachable.
    """
    llm_service = os.getenv('LLM_SERVICE_URL', 'http://127.0.0.1:5001')
    try:
        import requests
        payload = {'prompt': prompt, 'history': history}
        r = requests.post(f"{llm_service.rstrip('/')}/generate", json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            # service returns generated_text
            return data.get('generated_text') or data.get('text') or str(data)
        else:
            # Surface error to logs
            try:
                err = r.json()
            except Exception:
                err = r.text
            return f"(LLM service error) {r.status_code}: {err}"
    except Exception as e:
        return f"(LLM service unreachable) {e}"


@main_bp.route('/api/chat', methods=['POST'])
def api_chat():
    maybe_dev_login()
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json or {}
    prompt = data.get('message')
    if not prompt:
        return jsonify({'error': 'message required'}), 400

    # Load recent history for context (last 10 messages)
    msgs = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.desc()).limit(10).all()
    history = []
    for m in reversed(msgs):
        history.append({'role': 'assistant' if m.role == 'assistant' else 'user', 'content': m.content})

    # Save student message
    student_msg = Message(user_id=current_user.id, role='student', content=prompt)
    db.session.add(student_msg)
    db.session.commit()

    ai_text = generate_ai_response(prompt, history=history)

    ai_msg = Message(user_id=current_user.id, role='assistant', content=ai_text)
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify({'reply': ai_text, 'timestamp': ai_msg.created_at.isoformat()})


@main_bp.route('/api/history', methods=['GET'])
def api_history():
    maybe_dev_login()
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized'}), 401
    msgs = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.asc()).all()
    out = []
    for m in msgs:
        out.append({'role': m.role, 'content': m.content, 'timestamp': m.created_at.isoformat()})
    return jsonify({'history': out})


@main_bp.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({'status': 'ok'})


@main_bp.route('/api/health/llm', methods=['GET'])
def api_health_llm():
    """Check LLM service health by calling its /health endpoint."""
    llm_service = os.getenv('LLM_SERVICE_URL', 'http://127.0.0.1:5001')
    try:
        import requests
        r = requests.get(f"{llm_service.rstrip('/')}/health", timeout=10)
        if r.status_code == 200:
            return jsonify(r.json())
        return jsonify({
            'status': 'error',
            'detail': f'LLM service returned {r.status_code}',
            'service_response': r.text
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'detail': f'Could not reach LLM service at {llm_service}: {e}'
        })
