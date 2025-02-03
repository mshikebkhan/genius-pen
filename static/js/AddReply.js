// Add reply on comment

function AddReply(button) {
    var comment_id = button.name;
    $("#id_add_reply_submit_button").prop("disabled", true);
    $("#id_add_reply_submit_button").addClass('is-loading'); 

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../add-reply/'+comment_id+'/',        
        data:{
            body:$('#id_reply_body').val(),
        },
        success:function(json){

            $("#id_add_reply_submit_button").removeClass('is-loading');
            $("#id_add_reply_submit_button").prop("disabled", false);

            if(json.status == "added"){

                var newreply =
                '<div id="id_new_reply"></div>'+
                 '<div class="box" id="id_reply_'+json.id+'" style="border-radius: 10px;">'+                         
                        '<article class="media" >'+
                        '  <figure class="media-left">'+
                        '    <p class="image is-64x64">'+
                        '    <a href="/profile" >'+
                        '      <img class="profile_pic" style="width:64px; height:64px;" src="'+json.profile_pic+'">'+
                        '      </a>'+
                        '    </p>'+
                        '  </figure>'+
                        '  <div class="media-content">'+
                        '    <div class="content">'+
                        '      <p>'+
                        '        <strong>'+
                        '    <a href="/profile" >'+            
                                json.user+
                        '        </a>'+
                        '        </strong> <small>'+
                        '          <span class="icon is-small"><i class="fa fa-clock-o"></i></span> 0 minutes ago'+
                        '        </small>'+
                        '        <br>'+
                                json.body+
                        '      </p>'+
                        '    </div>'+
                        '</div> '+
                        '<div class="media-right">'+
                        '    <button name="'+json.id+'" onclick="DeleteReply(this)" class="delete"></button>'+
                        '  </div>'+
                        '</article>'+
                        '</div>'
                        ;

                document.getElementById("id_add_reply_form").reset();

                if (document.getElementById("id_new_reply")){
                $("#id_new_reply").before(newreply);    
                } 
                else {
                    $("#id_for_empty").html(newreply);
                    $("#id_empty_text").remove();

                }

                
                var replies_count = document.getElementById("id_replies_count");
                var number = replies_count.innerHTML;
                number++;
                replies_count.innerHTML = number; 
                
                setTimeout(function() {
                alert('Your reply has been added successfully!')
                },10)


            } else if(json.status == "error"){
                alert("An error occured!"); 

            }   
        },

    });

};
