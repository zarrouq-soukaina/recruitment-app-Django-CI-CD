# recruitment-app-Django-CI-CD

-Architected & built a web application to get project owners in contact with candidates.
This app contains :
* A recommendation system using user collaborative filtering based on the algorithm K nearest neighbors (KNN).
* An AI chatbot (conversational robot) based on the Naive Bayes classifier.
* A real time chat.

# Tools:
- UML
- Python 3.9 (Pandas, NumPy, SciPy, Pillow, Requests,Chatterbot and others) 
- Django.
- Flake8 
- Github actions (build a ci cd workflow)
- PostgreSQL
- HTML/CSS/JS

# Steps:
windows
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
*database : (the used SGBD is postgresql "Pgadmin4" . the details of the database "name, port, password .." are in the file settings) 
- python manage.py makemigrations main
- python manage.py migrate
*add superuser : 
- python manage.py createsuperuser
- python manage.py runserver

