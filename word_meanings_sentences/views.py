import http
import json
import random
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
import requests
from word_meanings_sentences import models
from word_meanings_sentences.models import Makesentence, Score
from random_word import RandomWords
import re
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SentenceSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
# some global variables
randomword = ""
meaning = ""
alltimescore = 0

# login
def login(request):
    return render(request,'index.html')

# homapage function showing score
def home(request):
    flag = 0
    user = request.user
    flagscore = models.Score.objects.filter()   
    for i in flagscore:
        if i.user == user:
            flag = 1
    
    if flag == 0:
        chkscore = Score(
                            user=user, score=0)
        chkscore.save()
    user = request.user
    showscore = models.Score.objects.get(user=request.user)
    show = showscore.score
    
    args = {
        "show": show,
        
    }
    return render(request, 'home.html',args)

# ending a game session by returning to homepage
def end(request):
    global randomword, meaning
    randomword =""
    meaning =""
    # return redirect(f"/accounts/profile")
    return redirect(f"/home")

# calling two api, one for word, another for meaning/definition
def getword(request):
    
    # api call for words
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    WORDS = response.content.splitlines()
    word = random.choice(WORDS).decode()
    global randomword
    randomword = word
    
    # api call for meanings/definition
    conn = http.client.HTTPSConnection("wordsapiv1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "3edf7b5a71mshb18cb7601af0b1bp15d53ajsnbf3ed97aac62",
        'X-RapidAPI-Host': "wordsapiv1.p.rapidapi.com"
    }

    conn.request("GET", f"/words/{word}/definitions", headers=headers)

    res = conn.getresponse()
    data = res.read()
    result = data.decode("utf-8")
 
    resultdict = json.loads(result)
    
    defi = resultdict.get("definitions")
    if not defi:
        return redirect(f"/getword")
    if res is None:
        return redirect(f"/getword") 
    strdefi = str(defi[0])
    if strdefi is None:
        return redirect(f"/getword")
    global meaning
    meaning = strdefi
   
    return redirect(f"/start")

# saving the data from two apis and user input
def start(request):
    user = request.user
    random = randomword
    if request.method == 'POST':
        if user is not None:
            sentence = request.POST.get("sentence")
            length=len(sentence)
            if(length<=100):
                    new_sentence = Makesentence(
                        sentence=sentence, user=user, word=random, meaning=meaning)
                    temp = checkSentence(sentence)
                    # sen_chk = Makesentence.objects.filter(title=request.GET['sentence'])
                    # print(sen_chk)
                    if temp is True:
                        new_sentence.save()
                    else:
                        return render(request,'error.html')
                        # return HttpResponse("Your sentence does not contain the word. Please go back and try again.")
                    global alltimescore
                    editscore = models.Score.objects.get(user=request.user)
                    alltimescore = editscore.score
                    alltimescore = alltimescore + 1
                    editscore.score = alltimescore
                    editscore.save()
            else:
                    return HttpResponse("Sentence is too long. Max length is 100 characters. Please Try Again")
    args = {
        "random": random,
        "meaning":meaning,
  
    }
    return render(request, 'start.html',args)

# logout
def logout(request):
    
    auth_logout(request)
    
    return render(request,'index.html')

# showing leaderboard
def leaderboard(request):
    showLeaderboard = models.Score.objects.filter()
    sortedByScore = sorted(showLeaderboard, key=lambda x: x.score, reverse=True)
    print(sortedByScore)
    args = {
        "sortedByScore": sortedByScore,  
    } 
    return render(request,'leaderboard.html', args)

# check if the word is in the sentence or mispelled word is written
def checkSentence(sen):
    global randomword
    
    chksen = sen.lower().split()
    #res = re.sub(r'[^\w\s]', '', chksen)
    length = len(chksen)
    #print(res)
    print(type(chksen))
    for j in range(length):
        res = re.sub(r'[^\w\s]', '', chksen[j])
        if res == randomword:
            
            return True
       
# API views here
@api_view(['GET'])
def getSentence(request):
    if request.method == 'GET':
        sentence = Makesentence.objects.filter()
        serializer = SentenceSerializer(sentence , many=True)
    return Response(serializer.data)

def API_test(request):
    word_found = 1
    flag = 0
    flag2 = 0
    show_sen = ""
    temp_word = ""
    show_mean=""
    user = request.user
    if request.method == 'POST':
        if user is not None:
            word_for_sen = request.POST.get("word_for_sen")
            print(word_for_sen)
            flag = 1
    url = "http://127.0.0.1:8000/get"
   
    response = requests.get(url)
    result= json.loads(response.text)
    
    count = len(result)
    if flag>0:
        for i in range(count):
            if word_for_sen == result[i]['word']:
                # result contains word, sentence & meaning
                word_found = 1
                # print(result)
                show_sen = result[i]['sentence']
                temp_word = word_for_sen
                show_mean = result[i]['meaning']
                break
            else:
                word_found = 0
    args = {
        "show_sen":show_sen,
        "temp_word": temp_word,
        "show_mean":show_mean,
    }  
        
    if(word_found==1):
        return render(request, 'API_test.html', args)
    else:
        return render(request,'error2.html')