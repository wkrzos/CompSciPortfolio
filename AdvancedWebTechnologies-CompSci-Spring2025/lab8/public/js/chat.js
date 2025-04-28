(() => {
  const loginScreen = document.getElementById('login-screen');
  const chatScreen = document.getElementById('chat-screen');
  const nicknameInput = document.getElementById('nickname-input');
  const joinBtn = document.getElementById('join-btn');
  const roomsSelect = document.getElementById('rooms');
  const messagesList = document.getElementById('messages');
  const messageForm = document.getElementById('message-form');
  const messageInput = document.getElementById('message-input');
  const imageInput = document.getElementById('image-input');
  const typingIndicator = document.getElementById('typing-indicator');
  
  let userNick = '';
  let typingTimeout;
  
  joinBtn.addEventListener('click', () => {
    const nick = nicknameInput.value.trim();
    if (!nick) return;
    userNick = nick;
    window.socket.emit('set nickname', nick);
    loginScreen.style.display = 'none';
    chatScreen.style.display = 'block';
  });

  roomsSelect.addEventListener('change', () => {
    const room = roomsSelect.value;
    window.socket.emit('join room', room);
    messagesList.innerHTML = '';
  });

  messageForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (imageInput.files.length > 0) {
      const file = imageInput.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        window.socket.emit('image', reader.result);
      };
      reader.readAsDataURL(file);
      imageInput.value = '';
    }
    const text = messageInput.value.trim();
    if (text) {
      window.socket.emit('chat message', text);
      messageInput.value = '';
    }
    window.socket.emit('typing', false);
  });

  messageInput.addEventListener('input', () => {
    window.socket.emit('typing', true);
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
      window.socket.emit('typing', false);
    }, 1000);
  });

  function addSystem(msg) {
    const li = document.createElement('li');
    li.className = 'system';
    li.textContent = msg;
    messagesList.appendChild(li);
    scrollBottom();
  }

  function addMessage(data, isImage) {
    const li = document.createElement('li');
    li.className = 'message ' + (data.nick === userNick ? 'outgoing' : 'incoming');
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = `${data.nick} [${data.time}]`;
    li.appendChild(meta);
    if (isImage) {
      const img = document.createElement('img');
      img.className = 'message-image';
      img.src = data.img;
      li.appendChild(img);
    } else {
      const text = document.createElement('div');
      text.className = 'text';
      text.textContent = data.text;
      li.appendChild(text);
    }
    messagesList.appendChild(li);
    scrollBottom();
  }

  function scrollBottom() {
    messagesList.scrollTop = messagesList.scrollHeight;
  }

  window.socket.on('system message', addSystem);
  window.socket.on('chat message', (msg) => addMessage(msg, false));
  window.socket.on('image', (img) => addMessage(img, true));
  window.socket.on('typing', (data) => {
    typingIndicator.textContent = data.isTyping ? `${data.nick} is typing...` : '';
  });
})();