// Add cover with js         
        function AddCoverImage() {

			$("#id_add_cover_label").html('Busy..');

            var fileInput =  
                document.getElementById('id_add_cover'); 
              
            var filePath = fileInput.value; 

            var file = fileInput.files[0];
            var FileSize = file.size / 1024 / 1024; // in MB
              
            if (FileSize > 2 ) {

                alert('The maximum cover image size is 2 MB');
                fileInput.value = '';
                $("#id_add_cover_label").html('Change'); 
                return false; 

            }


            else  
            { 
                // Show image preview
                    var reader = new FileReader(); 
                    reader.onload = function(e) {
                        var output = document.getElementById('id_add_cover_preview');
                        output.src = reader.result;
                        $("#id_add_cover_label").html('Change'); 
                    }; 
                      
                    reader.readAsDataURL(fileInput.files[0]); 
                } 
          }
                   
  function onChangeAddCoverImage(){
   $("#id_add_cover").change( function() {AddCoverImage()});
  }
  $(document).ready(onChangeAddCoverImage);    