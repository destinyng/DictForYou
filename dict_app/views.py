from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
import requests
import json

headers = {
    'x-rapidapi-key': "d618ca8550msh9a1dee08485d665p14bd7ejsnda930a271781",
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }

# Create your views here.
def index(request):
    return render(request, 'index.html')

def loginandregister(request):
    return render(request, 'loginandregister.html')

def register(request):
    if request.method != 'POST':
        return redirect ('/login')
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else: 
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        #messages.info(request, "User registered; log in now")
    return redirect('/users/profile')
   


def login(request):
    if request.method != 'POST':
        return redirect('/login')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['first_name'] = logged_user.first_name
                request.session['last_name'] = logged_user.last_name
            return redirect('/users/profile')
        messages.error(request, "Email and password are incorrect")
        return redirect('/login')

def logout(request):
    request.session.flush()
    return redirect('/')


def process(request):
    if 'userid' in request.session:
        
        logged_user = User.objects.get(id=request.session['userid'])

        word_object_set = Word.objects.filter(
            content = request.POST['content'],
        )
        word = request.POST['content']
        if len(word_object_set) == 0:
            word_object = Word.objects.create(
                content = request.POST['content']
            )
            
            word_object.searched_by.add(logged_user)
            word_object.save()
            
            url_synonyms = "https://wordsapiv1.p.rapidapi.com/words/{}/synonyms".format(word)
            url_definitions= "https://wordsapiv1.p.rapidapi.com/words/{}/definitions".format(word)
            url_antonyms = "https://wordsapiv1.p.rapidapi.com/words/{}/antonyms".format(word)

            response = requests.request("GET", url_synonyms, headers=headers)
            response_synonyms = response.json()
            # for key in response_dict:
                # print (response_dict[key])
            if len(response_synonyms['synonyms']) !=0:
                for value in response_synonyms['synonyms']:
                    synonym = Synonym.objects.create(
                        content = value,
                        word = word_object
                    )
            
            response_word = requests.request("GET", url_definitions, headers=headers)
            response_definitions = response_word.json()
            if len(response_definitions['definitions']) !=0:
                for value in response_definitions['definitions']:
                    for key in value:
                        if key == 'definition':
                            definition = Definition.objects.create(
                                content = value[key],
                                word = word_object
                            )
            response_word_dict_1 = requests.request("GET", url_antonyms, headers=headers)
            response_antonyms = response_word_dict_1.json()
            if len(response_antonyms['antonyms']) !=0:
                for value in response_antonyms['antonyms']:
                    antonym = Antonym.objects.create(
                        content = value,
                        word = word_object
                    )

            return redirect('/words/{}'.format(word)) 

        else:
            word = word_object_set[0]
            
            if logged_user not in word.searched_by.all():
                word.searched_by.add(logged_user)

            return redirect('/words/{}'.format(word.content))

    else:
        word_object_set = Word.objects.filter(
            content = request.POST['content'],
        )
        word = request.POST['content']
        if len(word_object_set) == 0:
            word_object = Word.objects.create(
                content = request.POST['content']
            )    
        
            url_synonyms = "https://wordsapiv1.p.rapidapi.com/words/{}/synonyms".format(word)
            url_definitions= "https://wordsapiv1.p.rapidapi.com/words/{}/definitions".format(word)
            url_antonyms = "https://wordsapiv1.p.rapidapi.com/words/{}/antonyms".format(word)

            response = requests.request("GET", url_synonyms, headers=headers)
            response_synonyms = response.json()
            # for key in response_dict:
                # print (response_dict[key])
            for value in response_synonyms['synonyms']:
                synonym = Synonym.objects.create(
                    content = value,
                    word = word_object
                )
            
            response_word = requests.request("GET", url_definitions, headers=headers)
            response_definitions = response_word.json()
            for key in response_definitions:
                print(response_definitions[key])

            for value in response_definitions['definitions']:
                for key in value:
                    if key == 'definition':
                        print("TEST:: ", value[key])
                        definition = Definition.objects.create(
                            content = value[key],
                            word = word_object
                        )
            response_word_dict_1 = requests.request("GET", url_antonyms, headers=headers)
            response_antonyms = response_word_dict_1.json()
            for key in response_antonyms:
                print(response_antonyms[key])

            for value in response_antonyms['antonyms']:
                antonym = Antonym.objects.create(
                    content = value,
                    word = word_object
                )

        return redirect('/words/{}'.format(word))

def word(request, content):
    
    if 'userid' in request.session:
        
        logged_user = User.objects.get(id=request.session['userid'])
        word = Word.objects.filter(content = content)
        word_definition = Definition.objects.filter(word=word[0])
        word_synonym = Synonym.objects.filter(word=word[0])
        word_antonym = Antonym.objects.filter(word=word[0])

        context={
            'word' : word[0],
            'definitions' : word_definition,
            'synonyms' : word_synonym,
            'antonyms' : word_antonym,
            'user': logged_user

        }
        logged_user.save()
        return render(request, 'word.html', context)
    else:
        word = Word.objects.filter(content = content)
        word_definition = Definition.objects.filter(word=word[0])
        word_synonym = Synonym.objects.filter(word=word[0])
        word_antonym = Antonym.objects.filter(word=word[0])
        




        context={
            'word' : word[0],
            'definitions' : word_definition,
            'synonyms' : word_synonym,
            'antonyms' : word_antonym,
            'user': None

        }
    
        return render(request, 'word.html', context)

def profile(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        logged_user = User.objects.get(id=request.session['userid'])
        
        
        Word.objects.filter(user_that_like_word= logged_user)
        Word.objects.filter(searched_by= logged_user)
        
        
        # for word in words:
        #     print(word.user_that_like_word)
        #     if logged_user in word.user_that_like_word:
        #        user_liked.append[word]
        
        
        context ={
            'user': logged_user,
            'searched_words': Word.objects.filter(searched_by= logged_user),
            'my_words': Word.objects.filter(user_that_like_word= logged_user)
        }
        return render(request, 'profile.html',context)    

def like(request,wordid):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method == "POST":
        logged_user = User.objects.get(id=request.session['userid'])   
        word = Word.objects.get(id=wordid)
        liked_users = word.user_that_like_word
        liked_users.add(logged_user)

    return redirect('/users/profile')
    
def delete(request,wordid):
    to_delete = Word.objects.get(id=wordid)
    to_delete.delete()
    return redirect('/users/profile')