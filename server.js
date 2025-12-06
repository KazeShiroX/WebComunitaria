const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 4200;

// Servir archivos estáticos de Angular
app.use(express.static(path.join(__dirname, 'dist/web-comunitaria/browser')));

// Redirigir todas las rutas al index.html (para Angular routing)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist/web-comunitaria/browser/index.html'));
});

app.listen(PORT, () => {
    console.log(`✅ Frontend server running on port ${PORT}`);
});
