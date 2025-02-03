// Report reply

function ReportReply(a) { 
    var reply_id = a.name;
    document.getElementById("id_report_reply_a_"+reply_id).setAttribute( "onClick", "" );
    $("#id_report_reply_a_"+reply_id).addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../report-reply/'+reply_id+'/',        
        success:function(json){

            if(json.status == "reported"){
                document.getElementById("id_report_reply_icon_"+reply_id).setAttribute( "class", "fa fa-flag" );
                alert("The reply has been been reported successfully.\nGeniusPen team will check this reply.");
            }
            else if(json.status == "error"){
               alert("An error occured!")
            } 

        },

    });

};
