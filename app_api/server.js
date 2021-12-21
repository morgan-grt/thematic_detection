const express = require('express');
const app = express();
const path = require("path");
const multer = require('multer');
const port = 9090;
const hostname = "0.0.0.0";
const boolean_true_value = ['1', 'True', 'true', 'on'];
const boolean_false_value = ['0', 'False', 'false', 'off'];
const default_value = {
    "default_user_max_cpu": {
        "value" : -1,
        "type" : "int"
    },
    "default_user_max_size": {
        "value" : -1,
        "type" : "int"
    },
    "default_user_pretty": {
        "value" : "true",
        "type" : "boolean"
    }
};

const storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './api/upload/');
  },
  filename: function (req, file, callback) {
    let ext = file.originalname.substring(
        file.originalname.lastIndexOf('.'), 
        file.originalname.length);
    let timestamp = Date.now().toString(36);
    let id = Math.random().toString(36).substr(2, 8);
    let name = file.fieldname + '-' + timestamp + '-' + id;
    callback(null, name + ext);
  }
});
const upload = multer({ storage : storage}).single('userfile');

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

const get_value_type = (value, name) => {
    if (default_value[name].type == "int"){
        if (!isNaN(value))
            return parseInt(value);
    }
    else if (default_value[name].type == "boolean"){
        if (boolean_true_value.includes(value))
            return 'true';
        else if (boolean_false_value.includes(value))
            return 'false';
    }
    return default_value[name].value;
}

const get_user_value = (data, name) => {
    if (typeof data !== 'string' && data.length > 1){
        if (data[1] !== '')
            value = data[1];
        else
            return default_value[name].value;
    }
    else
        value = data;

    return get_value_type(value, name);
}

const api_work = (req, res) => {
    let filename = req.file.filename;
    let user_max_cpu = get_user_value(req.body.user_max_cpu, 'default_user_max_cpu');
    let user_max_size = get_user_value(req.body.user_max_size, 'default_user_max_size');
    let user_pretty = get_user_value(req.body.user_pretty, 'default_user_pretty');

    let arguments = {
        "filename":filename,
        "user_max_cpu":user_max_cpu,
        "user_max_size":user_max_size,
        "user_pretty":user_pretty
    };

    const { spawn } = require('child_process');
    const pyProg = spawn('python3', ['./api/python/main.py', JSON.stringify(arguments)]);
    pyProg.stdout.on('data', function(data) {
        console.log(data.toString());

        if (data.toString().includes('canDownload')) {
            req.app.set('filename', filename);
            res.redirect(`/download`);
        }
    });
}

app.get('/download', (req, res) => {
    const file = `./api/result/result-` + req.app.get('filename');
    res.download(file); // Set disposition and send it.
});

app.post('/upload', (req, res) => {
    upload(req, res, function(err) {
        if (! req.file) {
            console.log('No file was uploaded');
            return res.end('No file was uploaded');
        }
        if(err) {
            console.log('Error uploading file');
            return res.end('Error uploading file.');
        }
        console.log('File is uploaded');
        api_work(req, res);
    });
});

app.listen(port, hostname, () => console.info(`🚀 App listening on port ${port}`));