from django import forms 
from .models import Account

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class':'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
        
        
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Lastname'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
    
    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError(
                'password does not match'
            )
    