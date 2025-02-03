from django.core.exceptions import ValidationError

def CoverImageValidator(file):
    """Validate story cover size"""
    filesize = file.size
    if filesize > 1048576*2:
   	 raise ValidationError("The maximum file size is 2 MB")
    else:
   	 return file

