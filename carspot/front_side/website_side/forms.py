from django import forms
from .models import Post, Category
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
import datetime

#cats = [    ('Cars','Cars'),    ('Motorcycles','Motorcycles'),    ('Boats','Boats'),]


choices = Category.objects.all().values_list('name','name')
choices_list = []
for item in choices:
    choices_list.append(item)
print(choices_list)
all_users = User.objects.values()
username = all_users[0]['username']
username_list = [(username,username)]
print(username_list)


class EmailForm(forms.Form):
    title = forms.CharField(required=True)
    price = forms.CharField(required=True)
    name = forms.CharField(required=True)
    author = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','location','author','price','miles','fuelType','featured','itemStatus','color','description','engine','powerLocks','powerWindows','make','year','bodytype','transmission','alloyWheels','abs','air','radio','cd','bonnet','airBags','coolBox','powerSteering','category','image1','image2','image3','image4','image5')
        
        widgets = {            
            'title': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Please enter a title', 'type': 'text'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'muie', 'type': 'hidden'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter price'}),
            'miles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter miles'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter description'}),
            'make': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter brand'}),
            'year': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter year'}),
            'engine': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter year'}),
            'itemStatus': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select transmission'}),
            'bodytype': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select body type'}),
            'transmission': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select transmission'}),
            'fuelType': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select fuel type'}),
            'alloyWheels': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'abs': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'powerLocks': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'featured': forms.Select(attrs={'class': 'form-control'}),
            'powerWindows': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'air': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'radio': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'cd': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'bonnet': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'airBags': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'coolbox': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'powerSteering': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices_list, attrs={'class': 'form-control'}),
            #'image': forms.ImageField(),
            
        }
        #print(widgets)


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','location','price','miles','fuelType','featured','itemStatus','color','description','engine','powerLocks','powerWindows','make','year','bodytype','transmission','alloyWheels','abs','air','radio','cd','bonnet','airBags','coolBox','powerSteering','category','image1','image2','image3','image4','image5')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Please enter a title', 'type': 'text'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices_list, attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter price'}),
            'miles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter miles'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter color'}),
            'engine': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter engine size'}),
            'itemStatus': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter add status'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter description'}),
            'make': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter brand'}),
            'year': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter year'}),
            'itemStatus': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select transmission'}),
            'bodytype': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select body type'}),
            'transmission': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select transmission'}),
            'fuelType': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please select fuel type'}),
            'alloyWheels': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'abs': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'featured': forms.Select(attrs={'class': 'form-control'}),
            'powerLocks': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'powerWindows': forms.CheckboxInput(attrs={'class': 'form-control'}),            
            'air': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'radio': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'cd': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'bonnet': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'airBags': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'coolbox': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'powerSteering': forms.CheckboxInput(attrs={'class': 'form-control'}),
            #'image': forms.ImageField(),
            #'image1': forms.ImageField(),
            
        }
