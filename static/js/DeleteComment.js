function DeleteComment(button) {
    var commentid = button.name;
    var x = confirm('Are you sure you want to delete this comment?');

      if(x){
        $("#id_comment_"+commentid).addClass("is-hidden");

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url: '../../../delete-comment/'+commentid+'/',

        success:function(json){
            
            if(json.status == "deleted"){

            var comment = document.getElementById("id_comment_"+commentid);
            comment.remove();

            var comments_count = document.getElementById("id_comments_count");
            var number = comments_count.innerHTML;
            number--;
            comments_count.innerHTML = number; 


            setTimeout(function() {
                alert('Comment has been deleted successfully!')
                 },10) 

            } else if(json.status == "error"){
                $("#id_comment_"+commentid).removeClass("is-hidden");
                setTimeout(function() {
                alert('Unable to delete an unknown error occured!'); 
                },10) 
            }        
    
      
        },
    });
};
}

