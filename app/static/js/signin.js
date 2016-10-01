function validate(){
    var username = $("#username").val();
    var password = $("#password").val();
    
    if (username == ""){
        $("#usr").html("Username required");
        return false;
    }
    if (password == ""){
        $("#pwd").html("Password required");
        return false;
    }
    
    return true;
}

function removeTips(obj){ 
    if (obj.id == "username" && obj.value == ""){
        if ($("#usr").html() != ""){
            $("#usr").html("");
        }
    }  
    
    if (obj.id == "password" && obj.value == ""){
        if ($("#pwd").html() != ""){
            $("#pwd").html("");
        }
    }  
}