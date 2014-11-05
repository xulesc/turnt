/**
 * Author: Anuj Sharma
 */

var __FIELDS_RSSVIZ = ['title', 'author', 'content'];

function __get_entries(data) {
	return data['feed']['entries'];
}

// simple space tokenization
function __rssviz_tokenize(str) {
	return str.split(" ");
}

// combine words in array with separator
function __implode(data, sep) {
	return data.reduce(function(a, b) {
		  return a + sep + b;
	});
}

// ubber bad way. surley this can be done better!!
function __freq(tokens) {
	var ret = new Array();
	// init
	for(var i = 0; i < tokens.length; i++) {
		ret[tokens[i]] = 0;
	}		
	// count
	for(var i = 0; i < tokens.length; i++) {
		ret[tokens[i]] += 1;
	}		
	return ret;
}

function feed_to_str(feed_url) {
	 var feed = new google.feeds.Feed(feed_url);
	 feed.load(function (data) {
	     // to analyze returned value use console.dir(data);
	     var entries = __get_entries(data);
	     var frequencies = entries.map(function(y) {
	    	 	var entry_data = __FIELDS_RSSVIZ.map(function(x) { return y[x]; });
	    	 	return __freq(__rssviz_tokenize(__implode(entry_data, ' ')));
	    	 }
	     );
	     console.log(frequencies);
	 });
 }
 
 /**
  * unit tests
  */ 
feed_to_str('http://ws.kathimerini.gr/xml_files/latestnews.xml');
 