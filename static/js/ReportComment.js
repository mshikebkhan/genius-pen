// Report comment

function ReportComment(a) { 
    var comment_id = a.name;
    document.getElementById("id_report_comment_a_"+comment_id).setAttribute( "onClick", "" );
    $("#id_report_comment_a_"+comment_id).addClass("is-idle")
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },     
        type:'POST',
        url:'../../../report-comment/'+comment_id+'/',        
        success:function(json){

            if(json.status == "reported"){
                document.getElementById("id_report_comment_icon_"+comment_id).setAttribute( "class", "fa fa-flag" );
                alert("The comment has been been reported successfully.\nGeniusPen team will check this comment.");
            }
            else if(json.status == "error"){
               alert("An error occured!")
            } 

        },

    });

};
