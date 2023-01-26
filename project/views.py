from django.shortcuts import render, redirect
#from main.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, JsonResponse






#new
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


chatbot = ChatBot(
    'Norman',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        }
    ]
)



training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
training_data = training_data_quesans


response = chatbot.get_response("Sorry, I didn't understand your question ")
print(response)

trainer = ListTrainer(chatbot)
trainer.train(training_data) 



@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)


def home(request, template_name="home.html"):
	context = {'title': 'Chatbot Version 1.0'}
	return render(None,template_name, context)












# Create your views here.
#def home(request):
#    return render(request, 'home.html')

#def room(request, room):
#    username = request.GET.get('username')
#    room_details = Room.objects.get(name=room)
#    return render(request, 'room.html', {
#        'username': username,
#        'room': room,
#        'room_details': room_details
#    })

#def checkview(request):
#    room = request.POST['room_name']
#    username = request.POST['username']

#    if Room.objects.filter(name=room).exists():
#        return redirect('/'+room+'/?username='+username)
#    else:
#        new_room = Room.objects.create(name=room)
#        new_room.save()
#        return redirect('/'+room+'/?username='+username)

#def send(request):
#    message = request.POST['message']
#    username = request.POST['username']
#    room_id = request.POST['room_id']

#    new_message = Message.objects.create(value=message, user=username, room=room_id)
#    new_message.save()
#    return HttpResponse('Message sent successfully')

#def getMessages(request, room):
#    room_details = Room.objects.get(name=room)

#    messages = Message.objects.filter(room=room_details.id)
#    return JsonResponse({"messages":list(messages.values())})




def index(request):
    return render(request, '../templates/registration/index.html')

def homeCandidate(request):
    return render(request, '../templates/Candidate/candidate_home.html')

def homeProjectOwner(request):
    return render(request, '../templates/ProjectOwner/projectOwner_home.html') 

def homeAdmin(request):
    return render(request, '../templates/Admin/admin_home.html')  

def homeModerator(request):
    return render(request, '../templates/Moderator/moderator_home.html')   

