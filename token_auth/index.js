const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');
const path = require('path');
const uuid = require('uuid');
const onFinished = require('on-finished');

const port = 3000;
const domain = 'dev-dujfreb276bpey3g.us.auth0.com';
const clientId = 'voRbP8j6Kw5Z7okdkyMxax13sij76oBL';
const clientSecret = 'U9l8qWyFq74iNwpHt7V7doXQsKBm-m80oSk7j_jLiLv-pHGL1zRqjRYNd1RDbw0g';
const audience = `https://${domain}/api/v2/`;
const SESSION_KEY = 'Authorization';

const client = jwksClient({
    jwksUri: `https://${domain}/.well-known/jwks.json`
});

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const sessions = new Map();

// Start server
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});

// Redirect to authorization page on SSO provider
app.get('/login', (req, res) => {
    const redirectUri = encodeURIComponent('http://localhost:3000/callback');
    const url = `https://${domain}/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&response_mode=query`;
    res.redirect(url);
});

// Handle authorization callback
app.get('/callback', async (req, res) => {
    const { code } = req.query;
    if (!code) {
        return res.status(400).send('Authorization code not provided');
    }

    try {
        const tokenData = await exchangeCodeForToken(code);
        const sessionId = uuid.v4();
        sessions.set(sessionId, tokenData); // Store tokens in session
        res.json({ sessionId, tokenData });
    } catch (error) {
        console.error('Error exchanging code for token:', error);
        res.status(500).send('Error during token exchange');
    }
});

// Exchange code for token
async function exchangeCodeForToken(code) {
    const response = await axios.post(`https://${domain}/oauth/token`, {
        grant_type: 'authorization_code',
        client_id: clientId,
        client_secret: clientSecret,
        redirect_uri: 'http://localhost:3000/callback',
        code: code
    });
    return response.data;
}

// Token verification middleware
app.use((req, res, next) => {
    const sessionId = req.get(SESSION_KEY);
    const sessionData = sessions.get(sessionId);

    if (sessionData) {
        req.user = sessionData;
    }
    next();
});

// Protected route
app.get('/api/protected', (req, res) => {
    if (!req.user) {
        return res.status(401).send('Unauthorized');
    }
    res.json({ message: 'Access granted', user: req.user });
});

// Main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API login route
app.post('/api/login', (req, res) => {
    res.redirect('/login');
});

// Logout route 
app.get('/logout', (req, res) => {
    const sessionId = req.get(SESSION_KEY);
    sessions.delete(sessionId);
    res.redirect('/');
});

