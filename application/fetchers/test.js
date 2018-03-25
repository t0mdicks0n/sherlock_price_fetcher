var pack = function (str) {
var result = ''
var quantifier = str.length;

for (i = 0; i < quantifier; i += 2) { word = str[i]; if (((i + 1) >= quantifier) || typeof str[i + 1] === 'undefined') {
		word += '0';
	} else {
		word += str[i + 1];
	}
	result += String.fromCharCode(parseInt(word, 16));
}
return result;
};

var signUrl = function (urlDomain, urlPath, id, key) {
var time = Math.round(new Date().getTime() / 1000);
var firstParam = (urlPath.indexOf("?") >= 0) ? "&" : "?";

console.log('firstParam', firstParam)

var urlTmp = urlPath.replace(" ", "+") +
	firstParam +
	"aid=" + id +
	"&timestamp=" + time;

var s = urlTmp + key;
var t = btoa(this.pack(md5(s)));
var tokken = t.replace(/\+/g, ".").replace(/\//g,"_").replace(/=/g,"-");

return urlDomain + urlTmp + "&hash=" + tokken;
};

signUrl('http://uk.shoppingapis.kelkoo.com',
	'/V3/productSearch?query=ipod&sort=default_ranking&start=1&results=20&show_products=1&show_subcategories=1&show_refinements=1',
	'myId',
	'myKey'
);