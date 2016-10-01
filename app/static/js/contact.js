function validate(){
    var name = $("#name").val();
    var email = $("#email").val();
    var message = $("#message").val();
    
    if (name == ""){
        $("#e_name").html("Name required");
        return false;
    }
    if (email == ""){
        $("#e_email").html("Email required");
        return false;
    }else{
        var reg = /\w+[@]{1}\w+[.]\w+/;
        if(!reg.test(email)){
             $("#e_email").html("It's not an Email address");
             return false;
        }
    }
    if (message == ""){
        $("e_message").html("Message required");
    }
    
    return true;
}

function removeTips(obj){ 
    if (obj.id == "name" && obj.value == ""){
        if ($("#e_name").html() != ""){
            $("#e_name").html("");
        }
    }  
    
    if (obj.id == "email" && obj.value == ""){
        if ($("#e_email").html() != ""){
            $("#e_email").html("");
        }
    }
    
    if (obj.id == "message" && obj.value == ""){
        if ($("#e_message").html() != ""){
            $("#e_message").html("");
        }
    }
}