from django import forms
from .models import Uploadedfiles,Developer, Supervisor


class Form_upload_file(forms.ModelForm):
    # Here we create a class that inherits from ModelForm.
    class Meta:
    # We extend the Meta class of the ModelForm. It is this class that will allow us to define the properties of ModelForm.
        model = Uploadedfiles
    # We define the model that should be based on the form.
        exclude = ('date_created', 'last_connexion', )
        fields=('files','title','description')#,'app_user'
    # We exclude certain fields of this form. It would also have been possible to do the opposite. That is to say with the fields property,
    # we have defined the desired fields in the form.
        


class Form_Developers(forms.ModelForm):
    # Here we create a class that inherits from ModelForm.
    class Meta:
    # We extend the Meta class of the ModelForm. It is this class that will allow us to define the properties of ModelForm.
        model = Developer
    # We define the model that should be based on the form.
        exclude = ('date_created', 'last_connexion', )
      
    # We exclude certain fields of this form. It would also have been possible to do the opposite. That is to say with the fields property,
    # we have defined the desired fields in the form.


