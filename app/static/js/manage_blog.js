function validate(){
    var title = $("#title").val();
    var url_title = $("#url_title").val();
    var tags = $("#tags").val();
    var content = $("#content").val();
    
    if (title == ""){
        $("#e_title").html("Title required");
        return false;
    }
    if (url_title == ""){
        $("#e_url_title").html("URL_Title required");
        return false;
    }
    if (tags == ""){
        $("#e_tags").html("Tags required");
        return false;
    }
    if (content == ""){
        $("#e_content").html("Content required");
        return false;
    }
    
    return true;
}

function removeTips(obj){ 
    if (obj.id == "title" && obj.value == ""){
        if ($("#e_title").html() != ""){
            $("#e_title").html("");
        }
    }  
    
    if (obj.id == "url_title" && obj.value == ""){
        if ($("#e_url_title").html() != ""){
            $("#e_url_title").html("");
        }
    }
    
    if (obj.id == "tags" && obj.value == ""){
        if ($("#e_tags").html() != ""){
            $("#e_tags").html("");
        }
    }
    
    if (obj.id == "content" && obj.value == ""){
        if ($("#e_content").html() != ""){
            $("#e_content").html("");
        }
    }
}