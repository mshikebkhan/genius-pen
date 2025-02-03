// Follow _ Unfollow Category

function FollowCategory(button) { 
    var category_id = button.name
    document.getElementById("id_follow_category_button_"+category_id).setAttribute( "onClick", "" );
    $("#id_follow_category_button_"+category_id).addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../follow-category/'+category_id+'/',        
        success:function(json){

            if(json.status == "followed"){
                $("#id_follow_category_span_"+category_id).html("Following")
                document.getElementById("id_follow_category_button_"+category_id).setAttribute( "class", "button is-info");
                document.getElementById("id_follow_category_button_"+category_id).setAttribute( "onClick", "FollowCategory(this)");
                $("#id_follow_category_icon_"+category_id).html("check_circle");                

            }
            else if(json.status == "unfollowed"){
                $("#id_follow_category_span_"+category_id).html("Follow")
                document.getElementById("id_follow_category_button_"+category_id).setAttribute( "class", "button is-light");
                document.getElementById("id_follow_category_button_"+category_id).setAttribute( "onClick", "FollowCategory(this)");
                $("#id_follow_category_icon_"+category_id).html("add"); 
            } 

        },

    })

}
