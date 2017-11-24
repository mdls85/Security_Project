const express = require('express');
const jsonfile = require('jsonfile');
const fetch = require('node-fetch');
const bodyParser = require('body-parser');
const sha1 = require('sha1');
const jsonServer = require('json-server');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();
const randtoken = require('rand-token');
const path    = require("path");
const app = express();

server.use(middlewares);
app.use(express.static(__dirname));
app.use(bodyParser.json());

app.get('/',function(req,res){
	res.sendFile(path.join(__dirname+'/index.html'));
});


// POST method route
app.post('/login', async function (req, res) {
	
	let dbserver = "http://localhost:3000";
	
	try{
		const resp = await fetch(`${dbserver}/users`);
		const users = await resp.json();
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

app.listen(3001, () => console.log('Example app listening on port 3001!'));


