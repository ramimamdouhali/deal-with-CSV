def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext=os.path.splitext(value.name)[1]
    valid_extension=['.csv']
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension, Please... upload *.csv files')
