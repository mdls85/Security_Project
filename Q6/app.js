const jsonServer = require('json-server');
const https = require('https');
const fs = require('fs');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();
const path    = require("path");
const express = require("express");
const randtoken = require('rand-token');
const port = 3001;

var options = {
	key: fs.readFileSync('/etc/letsencrypt/live/snickdx.me/privkey.pem', 'ascii'),
	cert: fs.readFileSync('/etc/letsencrypt/live/snickdx.me/cert.pem', 'ascii')
};


server.use(jsonServer.bodyParser);
server.use(middlewares);
server.use(express.static('./'));


function isAuthorized(req, breakFun){
	// if(req.method === "GET")return true;
	//
	// if(req.method === "POST"){
	// 	console.log(req.body);
	// 	if(!req.body.hasOwnProperty("token")) {
	// 		console.log(req.body);
	// 		breakFun();
	// 	}else{
	// 		return req.body.token !== "null";
	// 	}
	// }
	console.log(req.body);
	return true;
	// return false;
}

// Add custom routes before JSON Server router
server.get('/echo', (req, res) => {
	res.jsonp(req.query)
});

server.get('/app',function(req,res){
	res.sendFile(path.join(__dirname+'/index.html'));
});


server.post('/login', (req, res) => {

	
	try{
		const users = JSON.parse(fs.readFileSync('db.json', 'utf8')).users;
		users.forEach(user=>{
			console.log(user);
			if(user.username === req.body.username && user.password === req.body.password){
				res.status(200);
				res.send(randtoken.generate(16))
			}else{
				console.log("bad login");
				res.status(401);
				res.send("Incorrect Username/Password")
			}
		})
	}catch(error){
		console.log(error);
		res.status(500);
		res.send("Internal Server Error!");
	}
});


server.use((req, res, next) => {
	if (isAuthorized(req, res.send)) { // add your authorization logic here
		next() // continue to JSON Server router
	} else {
		res.sendStatus(401);
	}
});

server.use(router);


https.createServer(options, server).listen(port, function() {
	console.log("App running on port: " + port);
});