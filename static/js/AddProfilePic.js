// Add profile pic with js         
        function AddProfilePic() {

			$("#id_add_profile_pic_label").html('Busy..');

            var fileInput =  
                document.getElementById('id_add_profile_pic'); 
              
            var filePath = fileInput.value; 

            var file = fileInput.files[0];
            var FileSize = file.size / 1024 / 1024; // in MB
              
            if (FileSize > 10 ) {

                alert('The maximum profile pic file size is 10 MB');
                fileInput.value = '';
                $("#id_add_profile_pic_label").html('Change'); 
                return false; 

            }


            else  
            { 
                // Show image preview
                    var reader = new FileReader(); 
                    reader.onload = function(e) {
                        var output = document.getElementById('id_add_profile_pic_preview');
                        output.src = reader.result;
                        $("#id_add_profile_pic_label").html('Change'); 
                    }; 
                      
                    reader.readAsDataURL(fileInput.files[0]); 
                } 
          }
                   
  function onChangeAddProfilePic(){
   $("#id_add_profile_pic").change( function() {AddProfilePic()});
  }
  $(document).ready(onChangeAddProfilePic);    