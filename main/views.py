from django.contrib.auth import login, logout,authenticate
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from .form import *
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.core.mail import EmailMessage
from django.views.generic import View
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError  
from .tokens import account_activation_token
from django.core.mail import EmailMessage 
from django.conf import settings
from .filters import *
from django.http import HttpResponseRedirect
from django.db.models import Case, When

from django.http import StreamingHttpResponse
from .utilities import create_notification
import pandas as pd 

from django.http import HttpResponse , JsonResponse , Http404

from django.db.models import Max

from hitcount.views import HitCountDetailView
#from django.views.generic import DetailView


def register(request):
    return render(request, '../templates/registration/register.html')


class moderator_register(CreateView):
    model = CustomUser
    form_class = ModeratorSignUpForm
    template_name = '../templates/Moderator/moderator_register.html'

    def form_valid(self, form):
        user = form.save()
        email=user.email
       
        
        current_site = get_current_site(self.request)
        email_subject = 'Active your Account'
        message = render_to_string('registration/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   }
                                   )
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                        email_subject, message,  settings.EMAIL_HOST_USER,to=[to_email]
            )
        email.send()
           

        login(self.request, user)
        return redirect('/')
        

class admin_register(CreateView):
    model = CustomUser
    form_class = AdminSignUpForm
    template_name = '../templates/Admin/admin_register.html'

    def form_valid(self, form):
        user = form.save()
        email=user.email
       
        
        current_site = get_current_site(self.request)
        email_subject = 'Active your Account'
        message = render_to_string('registration/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   }
                                   )
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                        email_subject, message,  settings.EMAIL_HOST_USER,to=[to_email]
            )
        email.send()
           

        login(self.request, user)
        return redirect('/')
        

class candidate_register(CreateView):
    model = CustomUser
    form_class = CandidateSignUpForm
    template_name = '../templates/Candidate/candidate_register.html'

    def form_valid(self, form):
        user = form.save()
        email=user.email
       
        
        current_site = get_current_site(self.request)
        email_subject = 'Active your Account'
        message = render_to_string('registration/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   }
                                   )
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                        email_subject, message,  settings.EMAIL_HOST_USER,to=[to_email]
            )
        email.send()
           
        login(self.request, user)
        return redirect('/')


class projectOwner_register(CreateView):
    model = CustomUser
    form_class = ProjectOwnerSignUpForm
    template_name = '../templates/ProjectOwner/projectOwner_register.html'

    def form_valid(self, form):
        user = form.save()
        email=user.email
       
        
        current_site = get_current_site(self.request)
        email_subject = 'Active your Account'
        message = render_to_string('registration/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   }
                                   )
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                        email_subject, message,  settings.EMAIL_HOST_USER,to=[to_email]
            )
        email.send()
           
        login(self.request, user)
        return redirect('/')

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                #return redirect('/')
                if user.is_active and user.is_Candidate:
                    return redirect('candidate') 
                elif user.is_active and user.is_Admin :
                    return redirect('adminProj') 
                elif user.is_active and user.is_Moderator:
                    return redirect('moderator') 
                elif user.is_active and user.is_ProjectOwner:
                    return redirect('projectOwner')  
            
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/registration/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/') 
    
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            
            
            try:
                adm = Admin.objects.get(user=user)
                
            except Admin.DoesNotExist:
                adm = None
            
            if  adm == None:
                room= RoomAdmin( member= user)
                room.save()
                adn = Admin.objects.all()
                for a in adn:
                    room.admins.add(a)
                    
                    
                    
            else :
                rm = RoomAdmin.objects.all()
                #a = Admin.objects.get(user=user)
                for roomAdmin in rm :
                    roomAdmin.admins.add(adm)
                    
            
                    
                
                
                
            
            return redirect('login')
        return render(request, '../templates/registration/activate_failed.html', status=401)


def homeProjectOwner(request):
    offers = Offer.objects.all()
    total_offers = offers.count()
    context = {'offers':offers, 
    'total_offers':total_offers}

    return render(request, 'templates/ProjectOwner/projectOwner_home.html', context)

def homeAdmin(request):
    offers = Offer.objects.all()
    total_offers = offers.count()
    cand = Candidate.objects.all()
    total_cand = cand.count()
    owners = ProjectOwner.objects.all()
    
    total_owners = owners.count()
    offersA = Offer.objects.filter(status_O='active')
    total_offersA = offersA.count()
    offersD = Offer.objects.filter(status_O='deactivate')
    total_offersD = offersD.count()
    moderators = CustomUser.objects.filter(is_Moderator=True)
    total_moderators = moderators.count()
    
    context = {'offers':offers, 
    'total_offers':total_offers,'cand': cand,'total_cand':total_cand,'owners':owners,'total_owners':total_owners,'offersA':offersA, 
    'total_offersA':total_offersA,'offersD':offersD, 
    'total_offersD':total_offersD,'moderators': moderators,'total_moderators':total_moderators}
    return render(request, 'Admin/admin_home.html', context) 



def offers(request):
    if request.user.is_authenticated:
        offers = Offer.objects.filter(status_O='active',owner = ProjectOwner.objects.get(pk=request.user.id)).order_by('-offerDate')
        popular_offers = Offer.objects.order_by('-hit_count_generic__hits')[:3]
        
        context={'offers':offers,
        'popular_offers': popular_offers
        }
        
        return render(request, 'Offer/offers.html', context)

def offerview(request, pk_test):
	offer = Offer.objects.get(id=pk_test)
	context = {'offer':offer}
	return render(request, 'Offer/offerview.html',context) 

#def offerviewC(request, pk_test): 
	#offer = Offer.objects.get(id=pk_test)
	#context = {'offer':offer}
	#return render(request, 'Offer/offerviewC.html',context)

class offerviewC(HitCountDetailView):
    model = Offer
    template_name = 'Offer/offerviewC.html'
    context_object_name = 'offer'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(offerviewC, self).get_context_data(**kwargs)
        context.update({
        'popular_offers': Offer.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context
#Candidats non authentifiés
class offerviewCNonAuth(HitCountDetailView):
    model = Offer
    template_name = 'Offer/offerviewCNon.html'
    context_object_name = 'offer'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(offerviewCNonAuth, self).get_context_data(**kwargs)
        context.update({
        'popular_offers': Offer.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


def offerviewO(request, pk_test):
	offer = Offer.objects.get(id=pk_test)
	context = {'offer':offer}
	return render(request, 'Offer/offerviewC.html',context) 


#fixed problems in ownerview and candidateview user_id et pk_test were switched

def Ownerview(request, pk_test):
    if request.user.is_authenticated:
        #owner = ProjectOwner.objects.get(pk_test=request.user.id)
        owner = ProjectOwner.objects.get(user_id=pk_test)
        context = {'owner':owner}
    return render(request, 'ProjectOwner/ownerview.html',context) 
def OwnerviewA(request, pk_test):
    
    owner = ProjectOwner.objects.get(user_id=pk_test)
    context = {'owner':owner}
    return render(request, 'ProjectOwner/ownerview.html',context) 
	
def Candidateview(request, pk_test):
	candidate = Candidate.objects.get(user_id=pk_test)

	context = {'candidate':candidate}
	return render(request, 'Candidate/candidateview.html',context)



def createOffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST,request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.owner = ProjectOwner.objects.get(pk=request.user.id)
            if obj.salary > 0 :
                   obj.paid = 'yes'
                   obj.save()
            else :
                   obj.paid = 'no' 
                   obj.save()
                   
            offer= Offer.objects.get(id=obj.id)
               #add team
            team= Team(offerT=offer, owner = obj.owner)
            team.save()
            #add offerCandidate
            
            offers = offerCandidate(ofr=offer)  
            offers.save()
            #create rejectedCandidate
            offersR = RejectedCandidates(ofr=offer)  
            offersR.save()
               #add room
            room= Room(team = team)
            room.save()
            c = CustomUser.objects.get(id=request.user.id)
            room.members.add(c)
            adn = Admin.objects.all()
            for a in adn:
                   us = CustomUser.objects.get(id = a.user.id) 
                   create_notification(request, us , 'NewOffer', extra_id=offer.id)
            messages.success(request, "Your offer, team and room were added successfully ", extra_tags='offer')
            return redirect('offers')  
    else:
        form = OfferForm()
    return render(request, 'Offer/create-offer.html', {
        'form': form
    })
    
    
    # download file


def download(request,file_pk):
    offer = Offer.objects.filter(id=file_pk)[0]
    filename = offer.descriptive
    name = str(filename).split('/')[-1]
    filelocal = 'Files/'+str(filename)

    file = open(filelocal) 

    def file_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                     break
        
    response = StreamingHttpResponse(file_iterator(filelocal))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="'+str(name)+'"'
    return response


def offersC(request):
    offers = Offer.objects.filter(status_O='active', is_closed= False)
    myFilter = OfferCFilter(request.GET, queryset=offers)
    offers = myFilter.qs
    
    context = {'offers':offers,'myFilter':myFilter} 
      
            
    return render(request, 'Offer/offerC.html', context)
#non authentifiés
def offersCNON(request):
    offers = Offer.objects.filter(status_O='active', is_closed= False)
    myFilter = OfferCFilter(request.GET, queryset=offers)
    offers = myFilter.qs
    
    context = {'offers':offers,'myFilter':myFilter} 
      
            
    return render(request, 'Offer/offersNonAuth.html', context)

def archivePostulate(request):
    if request.user.is_authenticated:
        userc = get_object_or_404(Candidate, user=request.user)
        offerca = offerCandidate.objects.filter(cand=userc)
        offerefus= RejectedCandidates.objects.filter(cand=userc)
        accept= Team.objects.filter(cand=userc)
        context = {'offerca':offerca, 'offerefus':offerefus,'accept':accept }  
    
    
    return render(request, 'Offer/archiveCandidate.html',context)
        

#Postulate
def createOfferC(request,pk):
     
        
    if request.user.is_authenticated:
        userc = get_object_or_404(Candidate, user=request.user)
        candid = offerCandidate.objects.filter(cand=userc, ofr=pk)
        if not candid:
            offercand=offerCandidate.objects.get(ofr=Offer.objects.get(id=pk))
            
            
            c = Candidate.objects.get(user=request.user)
            
            offercand.cand.add(c)
            of = Myrating(offer=Offer.objects.get(id=pk),rating = 5, user =request.user)
            of.save()
            offer = Offer.objects.get(id=pk) 
            create_notification(request, offer.owner.user, 'application', extra_id=offer.id)
            messages.success(request, "you have applied the offer successfully ", extra_tags='app')
             
            

            return redirect('offersC')
        else: 
            can = RejectedCandidates.objects.filter(cand=userc, ofr=pk)
            if not can:
                messages.error(request, 'You have already applied for the offer!', extra_tags='ref')
            else:
                messages.error(request, 'your application was not accepted', extra_tags='refus')
            return redirect('offersC')
        

    
        
def offersCandidate(request,pk):
    
    offers = offerCandidate.objects.get(ofr=pk)
    offer = Offer.objects.get(id=pk)
    
    cands = offers.cand.all() 
    
   
    context = {'cands':cands, 'offer':offer } 
    
    
    return render(request, 'Offer/offerCandidate.html',context)


    
    
    return render(request, 'Offer/offerCandidate.html',context)
def updateOffer(request, pk):

    offer = Offer.objects.get(id=pk)
    
    form = OfferForm(instance=offer)

    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, " offer updated successfully ", extra_tags='offer')
            return redirect('offers')

    context = {'form':form}
    return render(request, 'Offer/update-offer.html', context)

def deactivateOffer(request,pk):
    offer = Offer.objects.get(id=pk)
    if request.method == "POST":   
        offer.status_O = 'deactivate'
        offer.save()
        tm = Team.objects.get(offerT=offer)
        tm.status_T= 'deactivate'
        tm.save()
        rm = Room.objects.get(team=tm)
        rm.status ='deactivate'
        rm.save()
        messages.error(request, 'You have deactivated this offer and its team and room!', extra_tags='deactivate')
        return redirect('offers')

    context = {'item':offer}
    return render(request, 'Offer/deactivate.html', context)
def deactivateOffera(request,pk): 
    offer = Offer.objects.get(id=pk)
    if request.method == "POST":   
        offer.status_O = 'deactivate'
        offer.save()
        messages.error(request, 'You have deactivated this offer and its team and romm!', extra_tags='deactivate')
        u = offer.owner
        a = CustomUser.objects.get(id = u.user.id )
        tm = Team.objects.get(offerT=offer)
        tm.status_T= 'deactivate'
        tm.save()
        rm = Room.objects.get(team=tm)
        rm.status ='deactivate'
        rm.save() 
                   
        
        create_notification(request, a , 'Deactivate', extra_id=offer.id)
        return redirect('indexO')

    context = {'item':offer}
    return render(request, 'Offer/deactivateAdmin.html', context)
def closeOffera(request,pk):
    offer = Offer.objects.get(id=pk)
    if request.method == "POST":  
        offer.is_closed = True
        offer.save()
        u = offer.owner
        a = CustomUser.objects.get(id = u.user.id )
        messages.error(request, 'You have closed this offer!', extra_tags='close')
        create_notification(request, a , 'Close', extra_id=offer.id)
        return redirect('indexO')
    
    context = {'item':offer}
    return render(request, 'Offer/closeAdmin.html', context)


def closeOffer (request,pk):
    offer = Offer.objects.get(id=pk)
    if request.method == "POST":  
        offer.is_closed = True
        offer.save()
        messages.error(request, 'You have closed this offer!', extra_tags='close')
        return redirect('offers')
    
    context = {'item':offer}
    return render(request, 'Offer/close.html', context)

#def roomUser (request):
    
            





def offersCandidateAdmin(request,pk):
    
    offers = offerCandidate.objects.get(ofr=pk)
    offer = Offer.objects.get(id=pk)
    
    cands = offers.cand.all() 
    
   
    context = {'cands':cands, 'offer':offer } 
    
    
    return render(request, 'Offer/offerCandidateAdmin.html',context)
           
            
def team(request,pk):
    teams = Team.objects.get(offerT=pk)
    
    itemscount= teams.cand.all().count()
    teams.numb = itemscount
    context =  {'teams':teams}
   
    return render(request, 'team/team.html',context)

def Candidateteam(request,pk):
    try:
        teams =Team .objects.get(id=pk)
                
    except Admin.DoesNotExist:
        teams = None
    
    
    
    cands = teams.cand.all() 
   
    context = {'cands':cands}  
    
    return render(request, 'team/candidate.html',context)
def CandidateteamAdmin(request,pk):
    try:
        teams =Team .objects.get(id=pk)
                
    except Admin.DoesNotExist:
        teams = None
    
    
    
    cands = teams.cand.all() 
   
    context = {'cands':cands}  
    
    return render(request, 'team/candidateAdmin.html',context)


def Reject(request, pk,vk):
    ca =  Candidate.objects.get(user = pk)
    c = CustomUser.objects.get(id=pk)
    offer = Offer.objects.get(id = vk)
    offerR = RejectedCandidates.objects.get(ofr= offer)
    offerR.cand.add(ca)
    messages.success(request, " You have rejected a candidate now", extra_tags='offer')
    create_notification(request, c, 'refus', extra_id=offer.id)
    return redirect('offers')
    

def accepter(request,pk,vk):
    ca =  Candidate.objects.get(user = pk)
    c = CustomUser.objects.get(id=pk)
    offer = Offer.objects.get(id = vk)
    tm= Team.objects.get(offerT= offer)
    tm.cand.add(ca)
    room= Room.objects.get(team= tm)
    room.members.add(c)
    messages.success(request, "The candidate is accepted  now! ", extra_tags='offer')
    
    create_notification(request, c, 'accept', extra_id=c.id)
    return redirect('offers')
       

    

        
   
  
   
def delete(request, pk):
    cand = offerCandidate.objects.get(id=pk)
    adn = Admin.objects.all()
    for a in adn:
        us = CustomUser.objects.get(id = cand.user) 
        create_notification(request, us , 'refus')
    
    context = {'item':cand}
    return render(request, 'Offer/delete.html', context)
    
    
def updateCandidate(request, pk):

    candidate = Candidate.objects.get(id=pk)
    
    form = CandidateSignUpForm(instance=candidate)

    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('Candidate')

    context = {'form':form}
    return render(request, 'Candidate/candidate_register.html', context)

def updateOwner(request, pk):

    owner = ProjectOwner.objects.get(id=pk)
    
    form = ProjectOwnerSignUpForm(instance=owner)

    if request.method == 'POST':
        form = ProjectOwnerSignUpForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('projectOwner')

    context = {'form':form}
    return render(request, 'ProjectOwner/projectOwner_register.html', context)





####Admin
#show all candidates 
def indexC (request):
    var= Candidate.objects.all()
    context = {'var':var}
    return render(request, 'Candidate/indexC.html',context)

#show all owners
def indexP (request):
    var= ProjectOwner.objects.all()
    context = {'var':var}
    return render(request, 'ProjectOwner/indexP.html',context)

#show all offers
def indexO (request):
    var= Offer.objects.all()
    myFilter = OfferFilter(request.GET, queryset=var)
    var = myFilter.qs
        
    context = {'var':var,'myFilter':myFilter}
    return render(request, 'Offer/indexO.html',context)

#show all teams
def indexT (request):
    var= Team.objects.all()
    context = {'var':var}
    return render(request, 'team/indexT.html',context)
#Deactivate Team
def deactivateTeam(request,pk):
    team = Team.objects.get(id=pk)
    team.status_T = 'deactivate'
    team.save()
   
    context = {'item':team}
    messages.success(request, "You have deactivate the team successfully ", extra_tags='offer')
    return render(request, 'team/deactivate.html', context)

#Deactivate User
def deactivateUser(request,pk):
    u = CustomUser.objects.get(id=pk)
    u.status_U = 'deactivate'
    u.save()
    
   
    context = {'item':u} 
    messages.success(request, "You have deactivate the user successfully ", extra_tags='offer')
    return render(request, 'User/deactivate.html', context)
    return redirect('indexC')
def deactivateAccount(request,pk):
    u = CustomUser.objects.get(id=pk)
    u.status_U = 'deactivate'
    u.save()
    
   
    context = {'item':u} 
    messages.success(request, "You have deactivate the user successfully ", extra_tags='offer')
    return render(request, 'User/deactivateaccount.html', context)
    


#show the offers of one owners
def OfferOwner(request,pk):
    offers = Offer.objects.filter(owner=pk)
    
    context = {'offers':offers} 
    return render(request, 'Offer/offerOwner.html', context) 

#show the offers postulate by a candidate
def OfferPosul(request,pk):
    offers = offerCandidate.objects.filter(cand=pk)
    
    context = {'offers':offers} 
    return render(request, 'Offer/offers.html', context)
#show the teams of a candidate 
def teamsC(request,pk):
    c = Team.objects.filter(cand=pk)
    
    context = {'c':c} 
    return render(request, 'team/teamC.html', context)
#show the teams of a owner
def teamOwner(request,pk):
    try:
         teams = Team.objects.filter(owner=pk)
               
    except Admin.DoesNotExist:
               teams = None
    
    
    context = {'teams':teams} 
    return render(request, 'team/teamOwner.html', context)
#show the team of an offer
def teamOffer(request,pk):
    teams = Team.objects.get(offerT=pk)
    a = teams.cand.all()
    total = a.count()
    context = {'teams':teams, 'a': a, 'total': total}  
    return render(request, 'team/teamS.html', context)

#show all Moderator : 

def moderators(request):
    m = CustomUser.objects.filter(is_Moderator=True)
    context = {'m':m}
    return render(request, 'Admin/moderators.html', context)


####Moderator
#show all candidates 
def indexCC (request):
    var= Candidate.objects.all()
    context = {'var':var}
    return render(request, 'Candidate/indexCC.html',context)

#show all owners
def indexPP (request):
    var= ProjectOwner.objects.all()
    context = {'var':var}
    return render(request, 'ProjectOwner/indexPP.html',context)

#show all offers
def indexOO (request):
    var= Offer.objects.all()
    myFilter = OfferFilter(request.GET, queryset=var)
    var = myFilter.qs
        
    context = {'var':var,'myFilter':myFilter}
    return render(request, 'Offer/indexOO.html',context)

#show all teams
def indexTT (request):
    var= Team.objects.all()
    context = {'var':var}
    return render(request, 'team/indexTT.html',context)



#show the offers of one owners
def OfferOwnerR(request,pk):
    offers = Offer.objects.filter(owner=pk)
    
    context = {'offers':offers} 
    return render(request, 'Offer/offerOwnerR.html', context)

#show the offers postulate by a candidate
def OfferPosulL(request,pk):
    offers = offerCandidate.objects.filter(cand=pk)
    
    context = {'offers':offers} 
    return render(request, 'Offer/offersS.html', context)
#show the teams of a candidate 
def teamsCC(request,pk):
    c = Team.objects.filter(cand=pk)
    
    context = {'c':c} 
    return render(request, 'team/teamCC.html', context)
#show the teams of a owner
def teamOwnerR(request,pk):
    teams = Team.objects.filter(owner=pk)
    
    context = {'teams':teams} 
    return render(request, 'team/teamS.html', context)
#Candidate
#show the teams of a candidate 
def teamsCandidate(request):
    if request.user.is_authenticated:
         c = Team.objects.filter(cand=Candidate.objects.get(pk=request.user.id),status_T='active')
         context = {'c':c}  
         return render(request, 'team/teamCC.html', context)
     
#Owner 
def teamsOwner(request):
    if request.user.is_authenticated:
         c = Team.objects.filter(owner=ProjectOwner.objects.get(pk=request.user.id))
         context = {'c':c}  
         return render(request, 'team/teamsOwner.html', context)

#recommandation 
# To get similar offers based on user rating(postulate for the offer on not)
def get_similar(offer_name,rating,corrMatrix):
    similar_ratings = corrMatrix[offer_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings
# Recommendation Algorithm
def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
 
    offer_rating=pd.DataFrame(list(Myrating.objects.all().values()))
    new_user=offer_rating.user_id.unique().shape[0]
    current_user_id= request.user.id
	# if new user did not postulate any offer
    if current_user_id>new_user:
        offer=Offer.objects.get(id=1)
        q=Myrating(user=request.user,offer=offer,rating=0)
        q.save()
    userRatings = offer_rating.pivot_table(index=['user_id'],columns=['offer_id'],values='rating')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')
    user = pd.DataFrame(list(Myrating.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    offer_id_watched = [each[0] for each in user_filtered]
    similar_offers = pd.DataFrame()
    for offer,rating in user_filtered:
        similar_offers = similar_offers.append(get_similar(offer,rating,corrMatrix),ignore_index = True)
    offers_id = list(similar_offers.sum().sort_values(ascending=False).index)
    offers_id_recommend = [each for each in offers_id if each not in offer_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(offers_id_recommend)])
    offer_list=list(Offer.objects.filter(id__in = offers_id_recommend).order_by(preserved)[:10])
    context = {'offer_list': offer_list}
    return render(request, 'recommend/recommend.html', context)




#Notifications
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)
    extra_id = request.GET.get('extra_id', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('view_application', pk=notification.extra_id)
        elif notification.notification_type == Notification.APPLICATION:
            return redirect('offersCandidate', pk=notification.extra_id)
        elif notification.notification_type == Notification.NewOffer:
            return redirect('offerview', pk_test=notification.extra_id)
        elif notification.notification_type == Notification.ACCEPT:
            return redirect('teamsCandidate')
        elif notification.notification_type == Notification.Deactivate:
            return redirect('offers')
        elif notification.notification_type == Notification.Close:
            return redirect('offerview', pk_test=notification.extra_id)
        elif notification.notification_type == Notification.inscriptionC:
            return redirect('Candidateview', pk_test=notification.extra_id)
        elif notification.notification_type == Notification.inscriptionO:
            return redirect('ownerview', pk_test=notification.extra_id)
        elif notification.notification_type == Notification.refus:
            return redirect('offerviewC', pk_test=notification.extra_id)
            
    
    return render(request, 'notification/notifications.html')

#chat

#go to the specific room

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room, 
        'room_details': room_details
    })
        
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/main/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/main/'+room+'/?username='+username)
    
#show all the rooms of a user 
def roomUser (request):
    if request.user.is_authenticated:
         R = Room.objects.filter(members=CustomUser.objects.get(pk=request.user.id),status ='active')
         myFilter = RoomFilter(request.GET, queryset=R)
         R = myFilter.qs
         c = Room.objects.filter(members=CustomUser.objects.get(pk=request.user.id)).values_list('members', flat=True).all()
         RC = c.count()
         RA = RoomAdmin.objects.get(member = request.user.id )

         context = {'R':R,'myFilter':myFilter,'RC':RC, 'RA': RA}  
          
         return render(request, 'chat/rooms.html', context)
    
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    rm = Room.objects.get(id = room_id)

    new_message = Message.objects.create(value=message, user=username, room=rm)
    new_message.save()
   
    
    for m in rm.members.all() :
        a = CustomUser.objects.get(id = m)
        create_notification(request, a , 'message', extra_id=room.id)
    return HttpResponse('Message sent successfully')



def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

#chat between admon and users

#show the rooms for admins (admin with owners)
def roomAdminOwner (request):
    if request.user.is_authenticated:
         R = RoomAdmin.objects.filter(admins=Admin.objects.get(user=request.user))
         myFilter = RoomsAdminFilter(request.GET, queryset=R)
         R = myFilter.qs
    
    
      
         context = {'R':R,'myFilter':myFilter}  
         return render(request, 'chat/roomsAdmin.html', context)
     
#show the rooms for User (admin with owners)
def roomOwnerAdmin (request):
    if request.user.is_authenticated:
         RA = RoomAdmin.objects.get(member=CustomUser.objects.get(id=request.user.id))
         context = {'RA':RA}  
         return render(request, 'chat/roomsOwnerAdmin.html', context)
     
     
#go to the specific room

def roomAdmin(request, room):
    username = request.GET.get('username')
    room_details = RoomAdmin.objects.get(name=room)
    return render(request, 'chat/roomAdmin.html', {
        'username': username,
        'room': room, 
        'room_details': room_details
    })
        
def checkviewAdmin(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if RoomAdmin.objects.filter(name=room).exists():
        return redirect('/main/chat/'+room+'/?username='+username)
    else:
        new_room = RoomAdmin.objects.create(name=room)
        new_room.save()
        return redirect('/main/chat'+room+'/?username='+username)
    
def sendAdmin(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    rm = RoomAdmin.objects.get(id = room_id)

    new_message = MessageAdmin.objects.create(value=message, user=username, room=rm)
    new_message.save()
    
    
    create_notification(request, rm.member , 'message', extra_id=room.id)
    create_notification(request, rm.member , 'message', extra_id=room.id)
    
    return HttpResponse('Message sent successfully')



def getMessagesAdmin(request, room):
    room_details = RoomAdmin.objects.get(name=room)

    messages = MessageAdmin.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

#show all the rooms to the admin
def allrooms(request):
    R = Room.objects.all()
    myFilter = RoomFilter(request.GET, queryset=R)
    R = myFilter.qs
    

    context = {'R':R,'myFilter':myFilter}  
          
    return render(request, 'chat/indexR.html', context)

#show the room of a specific offer
def roomOffer(request,pk):
    
    R = Room.objects.get(team=pk)
   
    context = {'R':R}  
          
    return render(request, 'chat/roomoffer.html', context)

#Deactivate Room
def deactivateRoom(request,pk):
    u = Room.objects.get(id=pk)
    u.status = 'deactivate'
    u.save()
    
   
    context = {'item':u}
    return render(request, 'Room/deactivate.html', context)


    



        
        