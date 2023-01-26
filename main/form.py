from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.forms.models import ModelForm
from .models import *
from django.forms.widgets import NumberInput 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ModeratorSignUpForm(UserCreationForm):
    
    name = forms.CharField(required=True)
    email =forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email']

    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Moderator = True
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.status_U = True
        user.is_active = False
        user.save()
        mod = Moderator.objects.create(user=user)
        mod.save()
        return user


class AdminSignUpForm(UserCreationForm):
    
    name = forms.CharField(required=True)
    email =forms.EmailField(required=True) 
    #CHOICES = [
    #('Admin', 'Admin'),
    #('Moderator', 'Moderator'),
    #]
    #level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    #level = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email']
    #class Meta(UserCreationForm.Meta):
    #    model = CustomUser
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Admin = True
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.save()
        admin = Admin.objects.create(user=user)
        #admin.level=self.cleaned_data.get('level')
        admin.save()
        return user


class CandidateSignUpForm(UserCreationForm):
   
    
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)
    #field_C = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=CHOICES_f)
    skills = forms.CharField(required=True,max_length=100)
    experience = forms.CharField(required=True)
    interest = forms.CharField(required=True)
    Educational_background = forms.CharField(required=True)
    school_Level = forms.CharField(required=True)
    age = forms.IntegerField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Candidate = True
        #user.is_staff = True
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.status_U = True
        user.is_active = False
        user.username= self.cleaned_data.get('name')
        user.save()
        candidate = Candidate.objects.create(user=user)
        #candidate.field_C = self.cleaned_data.get('field_C')
        candidate.skills = self.cleaned_data.get('skills')
        candidate.experience = self.cleaned_data.get('experience')
        candidate.interest = self.cleaned_data.get('interest')
        candidate.educ_background = self.cleaned_data.get('Educational_background')
        candidate.schoolLevel = self.cleaned_data.get('school_Level')
        candidate.age = self.cleaned_data.get('age')
        candidate.save()
        return user

    


class ProjectOwnerSignUpForm(UserCreationForm):
   
    CHOICES_f = [
    ('Business', 'Business'),
    ('Engineering', 'Engineering'),
    ('Management', 'Management'),
    ('Marketing', 'Marketing'),
    ('Data science', 'Data science'),
    ('Electronics', 'Electronics'),
    ('Robotics', 'Robotics'),
    ('Administration', 'Administration'),
    ('Industry', 'Industry'),
    ('Design', 'Design'),
    ('Software', 'Software'),
    ]

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)
    #field_P = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=CHOICES_f)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email']
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_ProjectOwner = True
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.status_U = True
        user.is_active = False
        user.username= self.cleaned_data.get('name')
        user.save()
        projectOwner = ProjectOwner.objects.create(user=user)
        #projectOwner.field_P = self.cleaned_data.get('field_P')
        projectOwner.save()
        return user
    
    
    

class OfferForm(ModelForm):
    start  = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    end  = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False)
    location = forms.CharField(required=False)

   
    class Meta:
        model = Offer
        fields = ['context', 'title', 'type','skills' , 'category','mode','start', 'end','location','salary','descriptive'] 
        
    CHOICES_f = [
    ('Business', 'Business'),
    ('Engineering', 'Engineering'),
    ('Management', 'Management'),
    ('Marketing', 'Marketing'),
    ('Data science', 'Data science'),
    ('Electronics', 'Electronics'),
    ('Robotics', 'Robotics'),
    ('Administration', 'Administration'),
    ('Industry', 'Industry'),
    ('Design', 'Design'),
    ('Software', 'Software'),
    ]
    category= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=CHOICES_f)
        

class OfferCForm(ModelForm):

    class Meta:
        model = offerCandidate
        fields = '__all__'
        