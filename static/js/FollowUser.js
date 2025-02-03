// Follow _ Unfollow User

function FollowUser(button) { 
    var user_id = button.name
    document.getElementById("id_follow_user_button_"+user_id).setAttribute( "onClick", "" );
    $("#id_follow_user_button_"+user_id).addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../follow-user/'+user_id+'/',        
        success:function(json){

            if(json.status == "followed"){
                $("#id_follow_user_button_"+user_id).html("<b>Following</b>")
                document.getElementById("id_follow_user_button_"+user_id).setAttribute( "class", "button is-rounded is-info is-small");
                document.getElementById("id_follow_user_button_"+user_id).setAttribute( "onClick", "FollowUser(this)");

                if (document.getElementById("id_followers_count")){
                var followers_count = document.getElementById("id_followers_count");
                var number = followers_count.innerHTML;
                number++;
                followers_count.innerHTML = number;     
                } 
                 
                if (document.getElementById("id_following_count")){
                var following_count = document.getElementById("id_following_count");
                var number = following_count.innerHTML;
                number++;
                following_count.innerHTML = number;     
                }

                $("#id_empty_text").remove();

            }
            else if(json.status == "unfollowed"){
                $("#id_follow_user_button_"+user_id).html("<b>Follow</b>")
                document.getElementById("id_follow_user_button_"+user_id).setAttribute( "class", "button is-rounded is-light is-small");
                document.getElementById("id_follow_user_button_"+user_id).setAttribute( "onClick", "FollowUser(this)");
            
                if (document.getElementById("id_followers_count")){
                var followers_count = document.getElementById("id_followers_count");
                var number = followers_count.innerHTML;
                number--;
                followers_count.innerHTML = number;     
                } 

                if (document.getElementById("id_following_count")){
                var following_count = document.getElementById("id_following_count");
                var number = following_count.innerHTML;
                number--;
                following_count.innerHTML = number;     
                }


            } 

        },

    })

}
