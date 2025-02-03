function OpenStoryMenu() {
      $("#id_story_menu").addClass("is-active");
      document.getElementById("id_story_menu_trigger").setAttribute( "onClick", "CloseStoryMenu()" );
};

function CloseStoryMenu() {
      $("#id_story_menu").removeClass("is-active");
      document.getElementById("id_story_menu_trigger").setAttribute( "onClick", "OpenStoryMenu()" );

};

