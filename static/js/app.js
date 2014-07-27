// Templates are loaded into this object
var ENV = {}
// the current location #hash is stored here
var HASH = ""

$(document).ready(function(){
	// Add handlebar helper for each
	Handlebars.registerHelper('each', function(context, options) {
		var ret = "";
		for(var i=0, j=context.length; i<j; i++) {
			ret = ret + options.fn(context[i]);
		}
		return ret;
	});
	
	// Load templates, and when done kick it off
	initTemplates(templateNames, function(){
		$(window).trigger("hashchange");
	})
});

function initTemplates(names, done) {
	for(n in names) {
		source = $("#template-"+names[n]).html()
		ENV[names[n]] = Handlebars.compile(source)
		Handlebars.registerPartial(names[n], source);
	}
	done()
}

// Fetch the current hash
function getHash() {
	hash = ""+window.location.hash;
	if(hash===null || hash=="") {
		return null
	}
	return hash.substring(1)
}

// Erase the current dom
function wipe() {
	$("#container").html("")
}

// Post-render callback
function done() {
	// If the current behavior has a ui counterpart, call it
	if(ui[HASH]) {
		ui[HASH]()
	}
}

$(window).bind('hashchange', function(e) {
	HASH = getHash();
	if(HASH == null) {
		HASH="index" // Default view
	}
	wipe();
	// Call up this hash's behavior
	if(behaviors[HASH]) {
		behaviors[HASH]()
	} else {
		behaviors["error"]("Unknown view!")
		hash="_error"
	}
	
	if(ui["_pageChange"]) {
		ui["_pageChange"](HASH)
	}
	
})

var behaviors = {
	error:function(message) {
		$("#container").append(ENV.error({message:message}));
	},
	index:function() {
		$.ajax("/api/getSomething", {dataType:"json", success:function(data){
			// Display a template on the page
			$("#container").append(ENV.index({people:data["people"]}));
			$("div.people > div").each(function(){
				$(this).on('click', function() {
					console.log("You clicked a row!");
				})
			})
			done()
		}});
	}
}
