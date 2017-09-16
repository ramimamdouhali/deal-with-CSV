from django import forms
from .models import Uploadedfiles,Developer, Supervisor
from django.contrib.auth.models import User


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
        widgets={
            
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})   
            }
        


class Form_Developers(forms.ModelForm):
    # Here we create a class that inherits from ModelForm.
    class Meta:
    # We extend the Meta class of the ModelForm. It is this class that will allow us to define the properties of ModelForm.
        model = Developer
    # We define the model that should be based on the form.
        exclude = ('date_created', 'last_connection', )
      
    # We exclude certain fields of this form. It would also have been possible to do the opposite. That is to say with the fields property,
    # we have defined the desired fields in the form.


class Form_Profile(forms.ModelForm):
    # Here we create a class that inherits from ModelForm.
    class Meta:
    # We extend the Meta class of the ModelForm. It is this class that will allow us to define the properties of ModelForm.
        model = Developer
    # We define the model that should be based on the form.
        fields=('phone','born_date')
        widgets={
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number', 'maxlength':'12',}),
            'born_date':forms.DateInput(attrs={'class':'form-control','placeholder':'Born Date'})   
        }
        labels={
            #'first_name': ('tryt'),
            
            }
        help_texts={
            
            }
        error_messages={
            'born_date':{'type':("max length")

            }
        }
        

    # We exclude certain fields of this form. It would also have been possible to do the opposite. That is to say with the fields property,
    # we have defined the desired fields in the form.

class Form_User(forms.ModelForm):
    # Here we create a class that inherits from ModelForm.
    class Meta:
    # We extend the Meta class of the ModelForm. It is this class that will allow us to define the properties of ModelForm.
        model = User
    # We define the model that should be based on the form.
        #exclude = ('date_created', 'last_connection', )
        fields=('first_name','last_name','email')
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
        }
        labels={
            #'first_name': ('tryt'),
            
            }
        help_texts={
            'email': ('Example: someone@domain.com'),
            }
        error_messages={
            'first_name':{'max_length':("longkkk")

            }
        }
        

        
        





