import django_filters
from django.forms.widgets import DateInput 
from .models import *

  
class OfferFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
    end = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
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
    category= django_filters.ChoiceFilter(choices=CHOICES_f)
    
    class Meta:
        model = Offer
		#fields = ('title','category','location','mode','salary')
        fields = ('owner','category','type','location','mode','paid','salary','start','end')
    
    
    
	

	
  
class OfferCFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
    end = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
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
    category= django_filters.ChoiceFilter(choices=CHOICES_f)
    
    class Meta:
        model = Offer
		#fields = ('title','category','location','mode','salary')
        fields = ('category','type','location','mode','paid','salary','start','end')
  
  
class OfferOwnerFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
    end = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
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
    category= django_filters.ChoiceFilter(choices=CHOICES_f)
    
    class Meta:
        model = Offer
		#fields = ('title','category','location','mode','salary')
        fields = ('category','type','location','mode','paid','salary','start','end')
	

	
  
class RoomsAdminFilter(django_filters.FilterSet):
    class Meta:
        model =RoomAdmin
		#fields = ('title','category','location','mode','salary')
        fields = ('member',)
  
class RoomFilter(django_filters.FilterSet):
	

	class Meta:
		model = Room
		#fields = ('title','category','location','mode','salary')
		fields = ('team',)

