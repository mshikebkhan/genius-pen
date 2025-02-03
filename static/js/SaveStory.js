// Save story

function SaveStory(a) { 
    var story_id = a.name;
    document.getElementById("id_save_story_a"+story_id).setAttribute( "onClick", "" );
    $("#id_save_story_a"+story_id).addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../save-story/'+story_id+'/',        
        success:function(json){

            if(json.status == "saved"){
                $("#id_save_story_icon"+story_id).html("bookmark")
                document.getElementById("id_save_story_a"+story_id).setAttribute( "onClick", "SaveStory(this)");
                $("#id_save_story_a"+story_id).removeClass("is-idle") 
            }
            else{
                $("#id_save_story_icon"+story_id).html("bookmark_border")
                document.getElementById("id_save_story_a"+story_id).setAttribute( "onClick", "SaveStory(this)");
                $("#id_save_story_a"+story_id).removeClass("is-idle")
            } 

        },

    });

};
