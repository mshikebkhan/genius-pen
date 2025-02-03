function DeleteReply(button) {
    var replyid = button.name;
    var x = confirm('Are you sure you want to delete this reply?');

      if(x){
        $("#id_reply_"+replyid).addClass("is-hidden");

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url: '../../../delete-reply/'+replyid+'/',

        success:function(json){
            
            if(json.status == "deleted"){

            var reply = document.getElementById("id_reply_"+replyid);
            reply.remove();

            var replies_count = document.getElementById("id_replies_count");
            var number = replies_count.innerHTML;
            number--;
            replies_count.innerHTML = number; 

            setTimeout(function() {
                alert('Reply has been deleted successfully!')
                 },10) 

            } else if(json.status == "error"){
                $("#id_reply_"+replyid).removeClass("is-hidden");
                setTimeout(function() {
                alert('Unable to delete an unknown error occured!'); 
                },10) 
            }        
    
      
        },
 
    });
};
}

