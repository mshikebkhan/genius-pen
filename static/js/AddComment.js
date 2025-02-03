// Add comment on story

function AddComment(button) {
    var story_id = button.name;
    $("#id_add_comment_submit_button").prop("disabled", true);
    $("#id_add_comment_submit_button").addClass('is-loading'); 

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../add-comment/'+story_id+'/',        
        data:{
            body:$('#id_comment_body').val(),
        },
        success:function(json){

            $("#id_add_comment_submit_button").removeClass('is-loading');
            $("#id_add_comment_submit_button").prop("disabled", false);

            if(json.status == "added"){


                    var newcomment =
                    '<div id="id_new_comment"></div>'+
                    '<div class="box" id="id_comment_'+json.id+'" style="border-radius: 10px;">'+                         
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
                    '        <br>'+
                    '        <small>'+
                    '           <a  href="/replies/'+json.id+'"><span class="icon is-small"><i class="fa fa-reply"></i></span> Replies 0</a>'+
                    '        </small>'+
                    '      </p>'+
                    '    </div>'+
                    '</div> '+
                    '<div class="media-right">'+
                    '    <button name="'+json.id+'" onclick="DeleteComment(this)" class="delete"></button>'+
                    '  </div>'+
                    '</article>'+
                    '</div>'
                    ;

                document.getElementById("id_add_comment_form").reset();

                if (document.getElementById("id_new_comment")){
                $("#id_new_comment").before(newcomment);    
                } 
                else {
                    $("#id_for_empty").html(newcomment);
                    $("#id_empty_text").remove();

                }

                var comments_count = document.getElementById("id_comments_count");
                var number = comments_count.innerHTML;
                number++;
                comments_count.innerHTML = number; 

                
                setTimeout(function() {
                alert('Your comment has been added successfully!')
                },10)

            } else if(json.status == "error"){
                alert("An error occured!"); 

            }   
        },

    });

};
