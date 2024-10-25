const uuid = require('uuid');
const express = require('express');
const onFinished = require('on-finished');
const bodyParser = require('body-parser');
const path = require('path');
const port = 3000;
const fs = require('fs');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');


const domain = 'dev-dujfreb276bpey3g.us.auth0.com'; 
const clientId = 'voRbP8j6Kw5Z7okdkyMxax13sij76oBL';
const clientSecret = 'U9l8qWyFq74iNwpHt7V7doXQsKBm-m80oSk7j_jLiLv-pHGL1zRqjRYNd1RDbw0g';
const audience = `https://${domain}/api/v2/`; // Аудиторія (API_IDENTIFIER)

const client = jwksClient({
    jwksUri: `https://${domain}/.well-known/jwks.json`
});

const SESSION_KEY = 'Authorization';
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})

const users = [
    {
        login: 'Login',
        password: 'Password',
        username: 'Username',
    },
    {
        login: 'Login1',
        password: 'Password1',
        username: 'Username1',
    },
    {
        login: 'DateArt',
        password: '2408',
        username: 'BoykoIPZ34ms',
        email: 'dima.boyko.bd@gmail.com',
    }
]

class Session {
    #sessions = {}

    constructor() {
        try {
            this.#sessions = fs.readFileSync('./sessions.json', 'utf8');
            this.#sessions = JSON.parse(this.#sessions.trim());

            this.#sessionDeleter(); 
            console.log('this session: ',this.#sessions);
        } catch(e) {
            this.#sessions = {};
        }
    }
    
    // Deletes empty sessions and removes duplicates
    #sessionDeleter() {
        const uniqueSessions = new Set();
        
        // Iterate over sessions to remove empty and duplicate ones
        Object.keys(this.#sessions).forEach((sessionId) => {
            const session = this.#sessions[sessionId];
            
            // Check if session is empty
            if (Object.keys(session).length === 0) {
                delete this.#sessions[sessionId]; // Delete empty session
            } else {
                // Create a unique identifier for non-empty sessions
                const sessionKey = `${session.username}-${session.login}`;
                
                // Check if session is a duplicate
                if (uniqueSessions.has(sessionKey)) {
                    delete this.#sessions[sessionId]; // Delete duplicate session
                } else {
                    uniqueSessions.add(sessionKey); // Mark session as seen
                }
            }
        });
        
        this.#storeSessions();
    }

    #storeSessions() {
        fs.writeFileSync('./sessions.json', JSON.stringify(this.#sessions), 'utf-8');
    }

    set(key, value) {
        if (!value) {
            value = {};
        }
        this.#sessions[key] = value;
        this.#storeSessions();
    }

    get(key) {
        return this.#sessions[key];
    }

    init(res) {
        const sessionId = uuid.v4();
        this.set(sessionId);

        return sessionId;
    }

    destroy(req) {
        const sessionId = req.sessionId;
        delete this.#sessions[sessionId];
        this.#storeSessions();
    }
}

const sessions = new Session();

app.use((req, res, next) => {
    let currentSession = {};
    let sessionId = req.get(SESSION_KEY);

    if (sessionId) {
        currentSession = sessions.get(sessionId);
if (!currentSession) {
            currentSession = {};
            sessionId = sessions.init(res);
        }
    } else {
        sessionId = sessions.init(res);
    }

    req.session = currentSession;
    req.sessionId = sessionId;

    onFinished(req, () => {
        const currentSession = req.session;
        const sessionId = req.sessionId;
        sessions.set(sessionId, currentSession);
    });

    next();
});

app.use('/api/secure', async (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
        return res.status(401).send('Access token required');
    }

    try {
        const decoded = await verifyToken(token);
        req.user = decoded;
        next();
    } catch (err) {
        console.error('Token verification failed:', err.message);
        res.status(401).send('Invalid token');
    }
});

app.get('/api/protected', async (req, res) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).send('Access token missing');

    try {
        const decoded = await verifyToken(token);
        res.json({ message: 'Access granted', user: decoded });
    } catch (error) {
        res.status(403).json({ message: 'Invalid token', error });
    }
});

app.get('/', (req, res) => {
    if (req.session.username) {
        return res.json({
            username: req.session.username,
            logout: 'http://localhost:3000/logout'
        })
    }
    res.sendFile(path.join(__dirname+'/index.html'));
})

app.get('/logout', (req, res) => {
    sessions.destroy(req, res);
    res.redirect('/');
});

app.post('/api/login', async (req, res) => {
    const { login, password } = req.body;

    const user = users.find((user) => {
        if (user.login == login && user.password == password) {
            return true;
        }
        return false
    });

    if (user) {
        req.session.username = user.username;
        req.session.login = user.login;

        const { access_token, id_token, refresh_token } = await getUserToken("dima.boyko.bd@gmail.com", "SomeStrongPassword1233");
        
        // Store the refresh token in the session for future use
        req.session.refresh_token = refresh_token;

        res.json({ access_token, id_token });
    } else {
        res.status(401).send('Unauthorized');
    }
});

app.post('/api/refresh', async (req, res) => {
    const refreshToken = req.session.refresh_token;

    if (!refreshToken) {
        return res.status(400).send('No refresh token found');
    }

    const { access_token, id_token } = await refreshAccessToken(refreshToken);

    // Update the session with the new tokens
    req.session.access_token = access_token;
    req.session.id_token = id_token;

    res.json({ access_token, id_token });
});


async function createUser(accessToken, email) {
    try {
        const response = await axios.post(`https://${domain}/api/v2/users`, {
            email: email,
            connection: 'Username-Password-Authentication',
            password: 'SomeStrongPassword1234',
            user_metadata: { role: 'user' }
        }, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('User Created:', response.data);
    } catch (error) {
        console.error('Error creating user:', error.response ? error.response.data : error.message);
    }
}

async function getAccessToken() {
    try {
        const response = await axios.post(`https://${domain}/oauth/token`, {
            audience: audience,
            grant_type: 'client_credentials',
            client_id: clientId,
            client_secret: clientSecret,
            scope: 'read:users',
        }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        const { access_token } = response.data;
        console.log('Access Token:', access_token);
        return access_token;
    } catch (error) {
        console.error('Error getting access token:', error.response ? error.response.data : error.message);
    }
}

async function getUserToken(username, password) {
    try {
        const response = await axios.post(`https://${domain}/oauth/token`, {
            grant_type: 'password',
            username: username,
            password: password,
            client_id: clientId,
            client_secret: clientSecret,
            audience: audience,  // The audience is the API identifier for the resource you're protecting
            scope: 'openid profile email offline_access', // Added 'offline_access' to request a refresh token
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const { id_token, refresh_token } = response.data;  

        console.log('ID Token:', id_token);  // This is the token that holds user identity information
        console.log('Refresh Token:', refresh_token);  // This is the refresh token you need

        return { id_token, refresh_token };
    } catch (error) {
        console.error('Error getting user token:', error.response ? error.response.data : error.message);
    }
}

async function getUsers(accessToken) {
    if (!accessToken) {
        console.error('Could not retrieve access token');
        return;
    }

    try {
        const response = await axios.get(`https://${domain}/api/v2/users`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        console.log('List of users:', response.data);
        return response.data; // This will be the list of users
    } catch (error) {
        console.error('Error fetching users:', error.response ? error.response.data : error.message);
    }
}

async function refreshAccessToken(refreshToken) {
    try {
        const response = await axios.post(`https://${domain}/oauth/token`, {
            grant_type: 'refresh_token',
            client_id: clientId,
            client_secret: clientSecret,
            refresh_token: refreshToken,
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const { access_token, id_token } = response.data;
        console.log('Refreshed Access Token:', access_token);
        console.log('New ID Token:', id_token);

        return { access_token, id_token };
    } catch (error) {
        console.error('Error refreshing access token:', error.response ? error.response.data : error.message);
    }
}

function getKey(header, callback) {
    client.getSigningKey(header.kid, (err, key) => {
        if (err) {
            callback(err);
        } else {
            const signingKey = key.getPublicKey();
            callback(null, signingKey);
        }
    });
}

function verifyToken(token) {
    return new Promise((resolve, reject) => {
        jwt.verify(token, getKey, { algorithms: ['RS256'] }, (err, decoded) => {
            if (err) {
                reject(err);
            } else {
                resolve(decoded);
            }
        });
    });
}

async function main() {
    const token = await getAccessToken();
    await createUser(token, 'dima.boyko.bd@gmail.com');

    getUsers(token);
}

main();
