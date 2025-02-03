// Like story

function LikeStory(a) { 
    var story_id = a.name
    document.getElementById("id_like_story_a").setAttribute( "onClick", "" );
    $("#id_like_story_a").addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../like-story/'+story_id+'/',        
        success:function(json){

            if(json.status == "liked"){
                $("#id_like_story_count").html(json.likes_count)
                $("#id_like_story_count2").html(json.likes_count)
                document.getElementById("id_like_story_icon").setAttribute( "class", "material-icons");
                document.getElementById("id_like_story_a").setAttribute( "onClick", "LikeStory(this)");
                $("#id_like_story_a").removeClass("is-idle")
                 
            }
            else if(json.status == "unliked"){
                $("#id_like_story_count").html(json.likes_count)
                $("#id_like_story_count2").html(json.likes_count)
                document.getElementById("id_like_story_icon").setAttribute( "class", "material-icons-outlined");
                document.getElementById("id_like_story_a").setAttribute( "onClick", "LikeStory(this)");
                $("#id_like_story_a").removeClass("is-idle")
            } 

        },

    })

}
