from django import forms

class Dateinput(forms.DateInput):
    input_type = 'date'

class FormCreateUser(forms.Form):
    CONTRY_CHOICES =(
    ("1", "Chile"),
    ("2", "Perú"),
    ("3", "Colombia"),
    ("4", "México"),
    ("5", "Brasil"),
    ("6", "Canadá"),
    ("7", "United States"),
    )

    ACCESS_CHOICE = (
    ("1", "NORMAL"),
    ("2", "EXECUTIVE"),
    ("3", "ADMIN"),
    ) 
    name = forms.CharField(max_length=150, required=True)
    user_name = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=300, required=True)
    nationality = forms.ChoiceField(choices=CONTRY_CHOICES)
    user_access =  forms.ChoiceField(choices=ACCESS_CHOICE)

class FormCreateMenu(forms.Form):
    fecha_menu = forms.DateField(widget=Dateinput, required=True)
    name_menu = forms.CharField(required= True, widget=forms.Textarea(attrs={'rows':15, 
                                                           'cols':50,     
                                                           'class':'form-control',
                                                           'style':'width: 49%;',                                                           
                                                           }))
class FormLogin(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': "login"}))
    password = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': "password",}))


     