document.querySelectorAll('.drawingX').forEach(canvas => {
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    function drawLinesToMouse(x, y) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(x, y);
        ctx.moveTo(canvas.width, 0);
        ctx.lineTo(x, y);
        ctx.moveTo(0, canvas.height);
        ctx.lineTo(x, y);
        ctx.moveTo(canvas.width, canvas.height);
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        drawLinesToMouse(x, y);
    });

    canvas.addEventListener('mouseleave', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });
});