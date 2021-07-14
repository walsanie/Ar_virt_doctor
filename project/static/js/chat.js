
$( document ).ready(function() {
    var time = formatAMPM(new Date());
    var firstBubble=' <li class="clearfix"> <div class="message-data align-right">'
    +'<span class="message-data-name" >Chatbot</span> <i class="fa fa-circle me"></i> <span class="message-data-time" >'
    +time
    +', Today</span> </div> <div id="chatbox" class="message other-message float-right"><p class="botText"><span>'
    +'مرحباً'
    +'</span></p></div> </li>';
    $("ul").append(firstBubble);


//alert("here");
    var me = {};
    var you = {};
    var response='';
    var user='';
    var time=0;

    function formatAMPM(date) {
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        minutes = minutes < 10 ? '0'+minutes : minutes;
        var strTime = hours + ':' + minutes + ' ' + ampm;
        return strTime;
    }


//-- No use time. It is a javaScript effect.

    function insertChat(who, text, time){
        var bubble = "";
        var date = formatAMPM(new Date());
        var time = formatAMPM(new Date());

        if (who == "me"){
             bubble= ' <li class="clearfix"> <div class="message-data align-right">'
                +'<span class="message-data-name" >Chatbot</span> <i class="fa fa-circle me"></i> <span class="message-data-time" >'
                +time
                +', Today</span> </div> <div id="chatbox" class="message other-message float-right"><p class="botText"><span>'
                +text
                +'</span></p></div> </li>';

        }else{
             bubble = '<li> <div class="message-data"> <span class="message-data-name"> <i class="fa fa-circle online"></i>User</span>'
                +'<span class="message-data-time">'
                + time
                + ', Today</span> </div> <div id="user_input" class="message my-message"> <p class="botText"><span >'
                + text
                +'</span></p></div></li>';

        }
        setTimeout(
            function(){
                $("ul").append(bubble);

            }, time);

    }

    function resetChat(){
        $("ul").empty();
    }

    $('#sendButton').click (function (){

        input = $("#user_in").val();

        $("#user_in").val("");
            user=insertChat("you",  input, 0);

        $.get("/get", {msg: input }).done(function(data) {
            response=insertChat("me",  data, 0);
        });
    });


});
