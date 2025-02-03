from django.core.exceptions import ValidationError

def ProfilePicSizeValidator(file):
    """Validate profile pic size"""
    filesize = file.size
    if filesize > 1048576*10:
   	 raise ValidationError("The maximum file size is 10 MB")
    else:
   	 return file

