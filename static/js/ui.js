var ui = {
	_pageChange: function(hash) {
		
	},
	_error:function() {
		
	},
	_modal:function(modal, content) {
		modal.find(".modal-body").html(content)
		modal.modal()
	},
	
	__streamstatus:function() {
		
	},
	index:function() {
		
	}
}
var validators = {
	samplevalidator: function(form) {
		messages = []
		
		if(form.find("input[name=name]").val()=="") {
			messages.push("Name must be entered");
		}
		
		if(messages.length==0) {
			return true
		}
		return messages
	}
}