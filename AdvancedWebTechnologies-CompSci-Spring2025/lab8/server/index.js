const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.use(express.static(__dirname + '/../public'));

io.on('connection', (socket) => {
  let userNick = '';
  let currentRoom = 'general';
  socket.join(currentRoom);

  socket.on('set nickname', (nick) => {
    userNick = nick;
    io.to(currentRoom).emit('system message', `${userNick} joined the chat`);
  });

  socket.on('join room', (room) => {
    socket.leave(currentRoom);
    io.to(currentRoom).emit('system message', `${userNick} left the room`);
    currentRoom = room;
    socket.join(currentRoom);
    io.to(currentRoom).emit('system message', `${userNick} joined the room`);
  });

  socket.on('chat message', (msg) => {
    const msgData = { nick: userNick, text: msg, time: new Date().toLocaleTimeString() };
    io.to(currentRoom).emit('chat message', msgData);
  });

  socket.on('typing', (isTyping) => {
    socket.to(currentRoom).emit('typing', { nick: userNick, isTyping });
  });

  socket.on('image', (data) => {
    const imgData = { nick: userNick, img: data, time: new Date().toLocaleTimeString() };
    io.to(currentRoom).emit('image', imgData);
  });

  socket.on('disconnect', () => {
    io.to(currentRoom).emit('system message', `${userNick} disconnected`);
  });
});

const PORT = process.env.PORT || 3000;
http.listen(PORT, () => console.log(`Server running on port ${PORT}`));