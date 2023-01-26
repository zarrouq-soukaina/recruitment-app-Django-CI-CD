from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

import random
from django.contrib.contenttypes.models import ContentType
from django.views import generic
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40,null=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    is_Moderator = models.BooleanField(default=False)
    is_Admin = models.BooleanField(default=False)
    is_Candidate = models.BooleanField(default=False)
    is_ProjectOwner = models.BooleanField(default=False)
    name = models.CharField(max_length=40,null=True)
    phone =  models.IntegerField(null=True)
    status_U = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        
        return f' {self.name}  '
    

class Admin (models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    
    def __str__(self):
        
        return f' {self.user.name} '
    
    
class Moderator (models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    
    def _str_(self):
        
        return f' {self.user.name} '
    

class Candidate (models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    #field_C =  models.CharField(max_length=80, null=True)
    skills = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    interest = models.CharField(max_length=100, null=True)
    educ_background = models.CharField(max_length=100, null=True)
    schoolLevel  = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    
    def __str__(self):
        
        return f' {self.user.name}  '
  
  

class ProjectOwner (models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    #field_P =  models.CharField(max_length=80, null=True)
    def __str__(self):
        return f' {self.user.name}  '

#class category(models.Model):
     
class Offer(models.Model, HitCountMixin):
   
    mode_CHOICES = [('In person','In person'),
                    ('Remote','Remote'),
                   
                    ]
    paid_CHOICES = [('yes','yes'),
                    ('no','no'),
                   
                    ]
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
    t_CHOICES = [('internship','internship'),
                    ('Pre-employment training','Pre-employment training'),
                    ('job','job'),
                   
                    ]
     
    mode = models.CharField(max_length=20,choices= mode_CHOICES, null=True)
    type = models.CharField(max_length=40,choices= t_CHOICES, null=True)
    offerDate= models.DateField(default=datetime.now)
    context= models.TextField(max_length=400, null=True)
    
    category= models.CharField(max_length=80, null=True)
    status_O = models.CharField(default='active',max_length=20)
    owner = models.ForeignKey(ProjectOwner, on_delete=models.CASCADE)
    #nmbreInterested=models.IntegerField(default=0, blank=True, null=True)
    #duration = models.CharField(max_length=10, null=True)
    salary = models.IntegerField( blank=True)
    is_closed = models.BooleanField(default=False)
    location = models.CharField(max_length=300,null=True)  
    title= models.CharField(max_length=50, null=True)  
    skills = models.CharField(max_length=50, null=True)
    start =  models.DateField(max_length=30, null=True)
    end =  models.DateField(max_length=30, null=True)
    descriptive=models.FileField(upload_to='./', null=True)
    paid = models.CharField(max_length=20,choices= paid_CHOICES, null=True)

    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    def __str__(self):
        return f'  {self.title} '
    
class Myrating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    
    

  
class  offerCandidate (models.Model):
  statusOC =models.CharField(default='active',max_length=20)
  ofr = models.ForeignKey(Offer, on_delete=models.CASCADE)
  cand =models.ManyToManyField(Candidate) 
  
 
  
class  RejectedCandidates (models.Model):
  status =models.CharField(default='active',max_length=20)
  ofr = models.ForeignKey(Offer, on_delete=models.CASCADE)
  cand =models.ManyToManyField(Candidate) 
  
  

  
class  Team (models.Model):
    numb = models.IntegerField(default=0, blank=True, null=True)
    status_T = models.CharField(default='active',max_length=20)
    cand =models.ManyToManyField(Candidate) 
    offerT = models.ForeignKey(Offer,on_delete=models.CASCADE)
    owner = models.ForeignKey(ProjectOwner, on_delete=models.CASCADE, null=True)
    def __str__(self):
        
        return f' {self.offerT}  '
    




#Notification

class Notification(models.Model):
    MESSAGE = 'message'
    APPLICATION = 'application'
    ACCEPT = 'accept'
    NewOffer = 'NewOffer' 
    Deactivate = 'Deactivate'
    Close = 'Close'
    inscriptionC = 'inscriptionC'
    inscriptionO = 'inscriptionO'
    refus = ' refus'

    CHOICES = (
        (MESSAGE, 'Message'),
        (APPLICATION, 'Application'),
        (ACCEPT, 'Accept'),
        (NewOffer, 'NewOffer'),
        (Deactivate, 'Deactivate'),
        (Close, 'Close'),
        (inscriptionO, 'inscriptionO'),
        (inscriptionC, 'inscriptionC'),
        (refus, 'refus'),
    )

    to_user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        
def random_string():
    return str(random.randint(10000, 99999))
        
#Room
class Room(models.Model):
    name = models.CharField(max_length=64,default = random_string)
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    members = models.ManyToManyField(CustomUser, blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(default='active',max_length=20)
    
    



class Message(models.Model):
    
    
    
    room = models.ForeignKey(Room, on_delete = models.CASCADE, null = True)
    value = models.CharField(max_length=5000,null = True) 
    
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000, null = True)
#chat admin

class RoomAdmin(models.Model):
    name = models.CharField(max_length=64,default = random_string)
    
    admins = models.ManyToManyField(Admin, blank=True)
    
    member = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = True )
    
#message with admin 
class MessageAdmin(models.Model):

    room = models.ForeignKey(RoomAdmin, on_delete = models.CASCADE, null = True)
    value = models.CharField(max_length=5000,null = True) 
    
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000, null = True)
    



    


