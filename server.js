const express = require('express');
const path = require('path');
const fileUpload = require('express-fileupload');
const { spawn } = require('child_process');

const app = express();

app.use(express.static(path.resolve(__dirname, 'src')));
app.use(fileUpload({
    limits: { fileSize: 100 * 1024 * 1024 },
}));

// Сама страница
app.get('/', async (req,res) => {
    res.sendFile(path.resolve(__dirname, 'src'));
});

// Текущая картинка
app.get('/current', async (req,res) => {
    res.sendFile(path.resolve(__dirname, 'img', 'test.jpg'));
})

// Загружаем картинку
app.post('/upload', async (req,res) => {
    const file = req.files.file;
    try {
        // Скачиваем
        file.mv(path.resolve(__dirname, 'img', 'test.jpg'));
        // Гоняем питон
        const proc = spawn('python', ['../scripts/script_2.py'], { cwd : path.resolve(__dirname, 'img') });
        proc.on('exit', (code) => {
            if(code === 0) {
                // Все хорошо, отправляем результат
                res.sendFile(path.resolve(__dirname, 'img', 'Output', 'output0.jpg'));
            } else {
                // Были ошибки
                res.sendStatus(500);
            }
        });
        proc.on('error', () => { 
            // Скрипт сломался
            res.sendStatus(500)
        });
    } catch(ex) {
        // Не смогли загрузить файлы
        res.sendStatus(500);
    }
})

app.listen(4000, () => { console.log('Heh!') });
