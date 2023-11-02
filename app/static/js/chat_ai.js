
function load_messages(messages){
    var chat = document.getElementById("chatMessages");
    for (let i=0; i<messages.length;i++){
        var div_msg = document.createElement("div");
        if (messages[i].role == "user"){
            div_msg.classList.add("user-message");
        }
        else if (messages[i].role == "assistant" ){
            div_msg.classList.add("bot-message");
        }
        chat.appendChild(div_msg);
        div_msg.textContent = messages[i].value;
    }
}


function submit_request(request){
    var request = document.getElementById("userInput").value;
    var chat = document.getElementById("chatMessages");
    $.ajax({
        type: "POST",
        url: "/private/aichat",
        data: { data: request},
        success: function(response){            
            chat.innerHTML = '';
            load_messages(response);
            document.getElementById("userInput").value = '';
        }     
               
    });
    
}