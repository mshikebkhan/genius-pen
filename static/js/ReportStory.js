// Report story

function ReportStory(a) { 
    var story_id = a.name;
    document.getElementById("id_report_story_a").setAttribute( "onClick", "" );
    $("#id_report_story_a").addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../report-story/'+story_id+'/',        
        success:function(json){

            if(json.status == "reported"){
                $("#id_report_story_text").html("Reported");
                alert("The story has been been reported successfully.\nGeniusPen team will check this story.\n But if you have any copyright issue then contact us on contact.geniuspen@gmail.com .");
            }
            else if(json.status == "error"){
                alert("An error occured!")
            } 

        },

    });

};
