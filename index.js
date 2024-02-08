const fs = require('fs');
const path = require('path');
const express = require('express');
const app = express();
const https = require('https');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const jwt = require('jsonwebtoken');
const child_process = require('child_process');

app.set('case sensitive routing', true);
app.use(cookieParser());

// CSSSR.secorg //

app.get('/index_csssr.css', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/CSSSR_Page/css/index_csssr.css'));
});

// jwt secret key //
const secret = "tH1s_iS_mY_5eCr3t_kEy_f0r_JwT"
// Encode in base64 //
const base64Secret = Buffer.from(secret).toString('base64');
// Code names //
const codeNames = ["GrosTacos", "Dopamine", "SilverNachos", "Persephone", "Diamante", "Wagnered", "Seraphin"];
// Roles //
const roles = ["Scientist", "Informator", "Secret Agent", "Negotiator", "Hacker", "Weapon Specialist", "Analyst"]

app.get('/csssr.secorg/', (req, res) => {
    if (req.cookies.cookies == 'b239f88bf63d4e95b1b23c9db7d68b40666167f3') {
        let rand = Math.floor(Math.random() * codeNames.length);
        let codeName = codeNames[rand];
        let role = roles[rand];
        // Craft a JWT token //
        const header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        const payload = {
            "codeName": codeName,
            "role": role
        }

        const token = jwt.sign(payload, base64Secret, { header });

        res.cookie('jwt', token, { maxAge: 900000, httpOnly: true });

        res.sendFile(path.join(__dirname, '/public/CSSSR_Page/index.html'));
    } else {
        res.redirect('/404');
    }
});

app.get('/csssr.secorg/members/', (req, res) => {
    try {
        const token = req.cookies.jwt;
        const decoded = jwt.decode(token, { complete: true });
        if (decoded.header.alg !== "HS256") {
            res.status(403).send(`
            Invalid token algorithm
            <script>
                setTimeout(function() {
                    window.location.href = "/csssr.secorg/";
                }, 3000);
            </script>
            `);
        } 
        else if (codeNames.includes(decoded.payload.codeName)) {
            res.sendFile(path.join(__dirname, '/public/CSSSR_Page/members.html'));
        } 
        else if (decoded.payload.role === "Director" && decoded.payload.codeName === "SupremeLeader") {
            res.sendFile(path.join(__dirname, '/public/CSSSR_Page/SupremeLeader.html'));
        } 
        else {
            res.status(403).send(`
            Something went wrong, you will be redirected to the main page
            <script>
                setTimeout(function() {
                    window.location.href = "/csssr.secorg/";
                }, 3000);
            </script>
            `); 
        };
    } catch (error) {
        console.error(error);
        res.redirect('/404');
    }
});

// __SECRETPROJECT__ //

app.get('/__secretPROJECT__', (req, res) => {
    if (req.cookies.cookies !== 'b239f88bf63d4e95b1b23c9db7d68b40666167f3') {
        res.redirect('/404');
    } else {
        res.sendFile(path.join(__dirname, '/public/__secretPROJECT__/index.html'));    }
});

app.get('/zip_dossier', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/zip_dossier'));
});

// ADMIN ENDPOINT //

app.get('/AdminENDPOINT_CSSSR_WEBSITE', (req, res) => {
    if (req.cookies.cookies !== '7e3851aec784b51e47005966e4cd7c64f6fe591a') {
        res.redirect('/404');
    } else {
        res.sendFile(path.join(__dirname, '/public/AdminENDPOINT_CSSSR_WEBSITE/index.html'));
    }
});

app.get('/index_admin_csssr.css', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/AdminENDPOINT_CSSSR_WEBSITE/css/index_admin_csssr.css'));
});

// TIMESTAMP UPLOADER //

app.use(bodyParser.json()); // Add this line to handle JSON data
app.use(bodyParser.urlencoded({ extended: true })); 


app.post('/testConnectionWebPages', (req, res) => {
    const url = req.body.url;
    const command = 'curl -I ' + url;
    const curl = child_process.spawnSync(command, { shell: true });
    console.log(command);
    const output = curl.stdout ? curl.stdout.toString() : null;
    const error = curl.stderr ? curl.stderr.toString() : null;

    if (curl.status !== 0) { // Check if there was an error
        res.json([
            {
                "status": "ERROR",
                "url": url,
                "output": output,
            }
        ]);
    }
    else {
        res.json([
            {
                "status": "OK",
                "url": url,
                "timestamp": Date.now(),
                "HTTP CODE": output.split('\n')[0].split(' ')[1],
                "output": output
            }
        ]);
    }
});
    

app.post('/downloadTASK-S.L', (req, res) => {
    const others_notes = fs.readdirSync('./public/CSSSR_Page/TASKS_UPLOADER/');
    const formatted_notes = others_notes.map(note => {
        const timestamp = parseInt(note.split('.')[0]); // Assuming the filename is the timestamp
        return new Date(timestamp).toLocaleString();
    });
    console.log(req.body.text);
    const text = req.body.text;
    const timestamp = Date.now(); 
    const path = `./public/CSSSR_Page/TASKS_UPLOADER/${timestamp}.txt`;
    fs.writeFileSync(path, text);
    res.json([
        {
            "id": timestamp, 
            "path": path.slice(20),
            "status": "Sent",
            "date": new Date().toLocaleString(),
            "content": text
        },
        {
            "Last Notes": formatted_notes,
        }
    ])
});

app.get('/TASKS_UPLOADER:timestamp', (req, res) => {
    const timestamp = req.params.timestamp;
    const path = `./public/CSSSR_Page/TASKS_UPLOADER/${timestamp}.txt`;
    res.download(path);
});

app.use(express.static(path.join(__dirname, 'public')));

// VALIDATOR //

app.post('/flagSubmit', (req, res) => {
    const username = req.body.username;
    let flag = req.body.flag;
    let error = null;
    let correctFlags = 0;

    const correctFlagsArray = [
        "CLOG{1st_ch4ll3ng3_1s_4lw4ys_3asy}",
        "CLOG{2nd_flag_h1dd3n_1n_r4nd0m_pl4c3}",
        "CLOG{3rd_flag_l4st_ea5y_0ne!!!}",
        "CLOG{4th_V3rb_T4mpering_1N_A_NuTsh3ll}",
        "CLOG{5th_Wh0_1s_3mpl0y33_0f_th3_y34r?}",
        "CLOG{6th_Supr3m3_L34d3r_0f_jWt?}",
        "CLOG{7th_Fr0m_Intern_To_Adm1n_of_Csssr_Webs1te?}"
    ];

    const userFlags = flag.split('\n');
    let userCorrectFlags = [];

    for (let i = 0; i < userFlags.length; i++) {
        if (correctFlagsArray.includes(userFlags[i])) {
            correctFlags++;
            userCorrectFlags.push(userFlags[i]);
        }
    }

    if (username === '') {
        error = 'Please enter a username';
    }

    if (error) {
        res.json({ error });
    } else {
        res.json({ success: `${correctFlags} flags discovered by you ${username}, valid flags : ${userCorrectFlags}` });
    }
});

/// FLAG3 ///

app.get('/flag', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/json/useless.json'));
});

/// INTRANET ///

app.get('/intranetCompany', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/intranetCompany/index.html'));
});

app.get('/index_intra.css', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/intranetCompany/css/index_intra.css'));
});

app.get('/index_secret.css', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/__secretPROJECT__/css/index_secret.css'));
});

app.get('/dashboard.js', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/intranetCompany/js/dashboard.js'));
});



app.post('/intranetCompany/loginINTRANET', (req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    let error = null;

    if (req.body.username === '') {
        res.json({ error: 'Please enter a username' });
    } else if (req.body.password === '') {
        res.json({ error: 'Please enter a password' });
    } else if (username === 'debugONLY' && password === 'debugONLY') {
        res.cookie('cookies', '67b27879506e6863f8760faf4a183729b9777f81', { maxAge: 900000, httpOnly: true });
        res.redirect('/intranetCompany/debugONLY'); 
    } else if (username === 'REDACTED' && password === 'TEMPORARY_PASSWORD_69420') {
        res.cookie('cookies', 'b239f88bf63d4e95b1b23c9db7d68b40666167f3', { maxAge: 900000, httpOnly: true });
        res.redirect('/__secretPROJECT__/');
    } else if (username === 'ADMINCSSSR_WEBSITE' && password === '6173170799') {
        res.cookie('cookies', '7e3851aec784b51e47005966e4cd7c64f6fe591a', { maxAge: 900000, httpOnly: true });
        res.redirect('/AdminENDPOINT_CSSSR_WEBSITE/');
    } else {
        res.json({ error: 'Incorrect username or password' });
    }
});

app.get('/intranetCompany/loginINTRANET', (req, res) => {
    res.send(`
    <html>
    <head>
    <title>INTRANET</title>
    </head>
    <body>
    <h1>For authorized personnel only</h1>
    <p> We have set up a debugonly account for you to use, the username and password are both debugONLY</p>
    PS: <p hidden> CLOG{4th_V3rb_T4mpering_1N_A_NuTsh3ll}</p>
    </body>
    </html>
    `);
});

app.get('/intranetCompany/debugONLY', (req, res) => {
    const id_notes = req.query.id_notes;

    if (req.cookies.cookies === '67b27879506e6863f8760faf4a183729b9777f81') {
        res.sendFile(path.join(__dirname, '/public/intranetCompany/debugONLY.html'));
        // create a dictionary of notes by id_notes value
        let notes = {"c4ca4238a0b923820dcc509a6f75849b": "Employée très sympathique, de bons résultats, mais elle a tendance à se faire remarquer par ses blagues douteuses. Je ne sais pas si c'est une bonne chose pour l'image de l'entreprise.",
        "c81e728d9d4c2f636f067f89cc14862c": "Stagiaire très prometteur, il a su s'intégrer rapidement dans l'équipe et a fait preuve d'une grande motivation.",
        "eccbc87e4b5ce2fe28308fd9f2a7baf3": "Employé très sérieux, il a su faire preuve de professionnalisme et de rigueur. Je recommande.",
        "ad61ab143223efbc24c7d2583be69251" : "Nous avons sélectionné REDACTED pour ses aptitudes hors du commun. Je pense que c'est l'élément qui nous manquait pour faire décoller notre projet ... Lui transmettre ces instructions (/zip_dossier:mdp(ID+[space])) et le laisser travailler. Il saura quoi faire.",
        };
        if (id_notes in notes) {
            res.json(notes[id_notes]);
        }
    } else {
        res.redirect('/404');
    }
});

app.get('/intranetCompany/css/dashboard.css', (req, res) => {x
    res.sendFile(path.join(__dirname, '/public/intranetCompany/css/dashboard.css'));
});

app.get('/intranetCompany/js/dashboard.js', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/intranetCompany/js/dashboard.js'));
});

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/404.html'));
});

app.get('/404', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/404.html'));
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/index.html'));
});

app.listen(4567, () => {
    console.log('http://localhost:4567');
});