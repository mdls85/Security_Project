// server.js
const jsonServer = require('json-server');
const https = require('https');
const fs = require('fs');
const server = jsonServer.create();
const router = jsonServer.router('attackerdb.json');
const middlewares = jsonServer.defaults();
const express = require("express");

var options = {
	key: fs.readFileSync('/etc/letsencrypt/live/snickdx.me/privkey.pem', 'ascii'),
	cert: fs.readFileSync('/etc/letsencrypt/live/snickdx.me/cert.pem', 'ascii')
};

const port = 3002;

server.use(express.static('./'));

server.use(middlewares);
server.use(router);

https.createServer(options, server).listen(port, function() {
	console.log("Attacker running on port: " + port);
});