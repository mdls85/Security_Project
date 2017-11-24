const jsonServer = require('json-server');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();



function isAuthorized(req){
	if(req.method === "GET")return req.query.token !== "null";

	if(req.method === "POST")
		return req.body.hasOwnProperty("token") ? req.body.token !== "null" : false;
	
	return false;
}

server.use(jsonServer.bodyParser);
server.use(middlewares);
server.use((req, res, next) => {
	if (isAuthorized(req)) { // add your authorization logic here
		next() // continue to JSON Server router
	} else {
		res.sendStatus(401);
	}
});

server.use(router);
server.listen(3000, () => {
	console.log('JSON Server is running on port 3000')
});