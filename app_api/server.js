const express = require('express');
const app = express();
const path = require("path");
const multer = require('multer');
const port = 8080;
const hostname = "0.0.0.0";

const storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './api/upload/');
  },
  filename: function (req, file, callback) {
    let ext = file.originalname.substring(file.originalname.lastIndexOf('.'), file.originalname.length);
    callback(null, file.fieldname + '-' + Date.now() + ext);
  }
});
const upload = multer({ storage : storage}).single('filetoupload');

// Static Files
app.use(express.static('ui'));
// Specific folder example
app.use('/css', express.static(path.join(__dirname, 'ui/css')));
app.use('/js', express.static(path.join(__dirname, 'ui/js')));
app.use('/img', express.static(path.join(__dirname, 'ui/img')));

// Set View's
app.set('views', path.join(__dirname, "ui"));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

// Navigation
app.get('/', (req, res) => {
    res.render('index');
});

const api_work = (req, res) => {
    let filename = req.file.filename;
    const { spawn } = require('child_process');
    const pyProg = spawn('python3', ['./api/python/classifier.py', filename]);
    console.log('CALL');
    pyProg.stdout.on('data', function(data) {
        console.log('IN');
        console.log(data.toString());

        if (data.toString().includes('canDownload')) {
            console.log('PASS');
            req.app.set('filename', filename);
            res.redirect(`/download`);
        }
    });

}

app.get('/download', (req, res) => {
    const file = `./api/result/result-` + req.app.get('filename');
    res.download(file); // Set disposition and send it.
});

app.post('/fileupload', (req, res) => {
    upload(req, res, function(err) {
        console.log(req.file);
        if (! req.file) {
            console.log('No file was uploaded');
            return res.end('No file was uploaded');
        }
        if(err) {
            console.log('Error uploading file');
            return res.end('Error uploading file.');
        }
        console.log('File is uploaded');
        //res.write('File is uploaded');
        api_work(req, res);
    });
});

app.listen(port, hostname, () => console.info(`🚀 App listening on port ${port}`));