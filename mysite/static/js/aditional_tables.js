function aditionalTables(table,stock,id) {
    console.log(stock);
    console.log(table);
    console.log(id);
    console.log(id+1);
    var table_id = "table"+id;
    $.ajax( {
	url:'/tables/',
	timeout:5000,
	type: 'POST',
	data: {
	    "django_stock": stock,
            "django_table": table,
            "django_id": table_id,
	    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
	},
	success: function(data) {
            id = parseInt(id);
            console.log(id+1);
	    console.log("message");
	    console.log(data);
            var url = data["url"];
            var working = data["working"];
            if (working == "yes") {
                window.location = url;
            }
            else {console.log("No pdfs");}
	},
	error: function(xhr,errmsg,err) {
	    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	},
	traditional: true
    });
}
