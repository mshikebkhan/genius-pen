function OpenDraftMenu() {
      $("#id_draft_menu").addClass("is-active");
      document.getElementById("id_draft_menu_trigger").setAttribute( "onClick", "CloseDraftMenu()" );
};

function CloseDraftMenu() {
      $("#id_draft_menu").removeClass("is-active");
      document.getElementById("id_draft_menu_trigger").setAttribute( "onClick", "OpenDraftMenu()" );

};

