
#@pytest.mark.django_db #give test access to database  
# def test_user_create():    
#     # Create dummy data       
#     user = CustomUser.objects.create(username="Soukaina",email="zarrouqsoukaina@gmail.com", is_Moderator=False, is_Admin=False,is_Candidate=False,is_ProjectOwner= True,name="soukaina",phone="75859538350",status_U="active")    
#     # Assert the dummy data saved as expected       
#     assert user.username=="Soukaina"      
#     assert user.email=="zarrouqsoukaina@gmail.com"
#     assert user.is_Moderator== False
#     assert user.is_Admin== False
#     assert user.is_Candidate== False
#     assert user.is_ProjectOwner==True
#     assert user.name=="soukaina"
#     assert user.phone=="75859538350"
#     assert user.status_U=="active"
