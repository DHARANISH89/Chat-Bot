function fmt(ts){
  const d = new Date(ts);
  return d.toLocaleString();
}

function appendMessage(role, content, ts){
  const container = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = 'msg ' + (role === 'student' ? 'student':'assistant');
  el.innerHTML = `<div class="meta">${role} • ${fmt(ts)}</div><div class="content">${content.replace(/\n/g,'<br/>')}</div>`;
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

document.getElementById('chatForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const input = document.getElementById('messageInput');
  const text = input.value.trim();
  if(!text) return;
  appendMessage('student', text, new Date().toISOString());
  input.value = '';

  const res = await fetch('/api/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:text})});
  if (!res.ok){
    appendMessage('assistant', '(error) Could not get response', new Date().toISOString());
    return;
  }
  const j = await res.json();
  appendMessage('assistant', j.reply, j.timestamp || new Date().toISOString());
});

document.getElementById('historyBtn').addEventListener('click', async ()=>{
  const res = await fetch('/api/history');
  if (!res.ok) return alert('Could not load history');
  const j = await res.json();
  const container = document.getElementById('messages');
  container.innerHTML = '';
  j.history.forEach(m => appendMessage(m.role, m.content, m.timestamp));
});

document.getElementById('newChat').addEventListener('click', ()=>{
  document.getElementById('messages').innerHTML = '';
});
