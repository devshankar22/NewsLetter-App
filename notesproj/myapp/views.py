from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from newsapi import NewsApiClient
import json
from datetime import datetime
from django.contrib import messages
from django.views.decorators.cache import cache_control
import requests
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True)
def home(req):
    return redirect('news')



def login(req):
 if req.method=='POST':
  print('devshankar',req.POST)
  try:
   d=dict(req.POST)
   #print(d)
   print(d['username'])
   print('devshankar')
   user=auth.authenticate(username=d['username'][0],password=d['password'][0])
   print("hi")
   if user is not None:
    auth.login(req, user)
    return redirect('/')
   else:
    messages.error(req,'account not found')
    return redirect('login')
  except Exception as e:
   print('\n\n',str(e),'\n\n')
   return redirect('news') 
 return redirect('news')

def signup(req):
 if 'signup' in req.POST:
  d=req.POST
  #o=login.objects.create(logid=d['logid'],password=d['password'],name=d['name'],branch=d['branch'],sem=d['sem'])
  try:   
   s=User.objects.get(username=d['username'])
   return HttpResponse('this username already exist')
  except Exception as e:
   #o=Login(logid=d['logid'],password=d['password'],name=d['name'],branch=d['brn'],sem=d['sem'])
   o=Login.objects.create(username=d['username'],email=d['email'],password=d['password'],name=d['name'])
   o.save()
   user=User.objects.create_user(username=d['username'],password=d['password'])
   user.first_name=d['name']
   user.last_name=''
   user.save()
   mm='Hello '+d['name']+'<br><br>Your Personal Details(Don\'t share to anyone)<br><br>Username: '+d['username']+'<br>Password: '+d['password']+'<br><br>Welcome to our Aspire News Application'
   send_mail('Aspire News','',settings.EMAIL_HOST_USER,[d['email']],html_message=mm)
   return redirect('/')
 return render(req,'signup2.html',{})

@login_required(login_url='login')
def logout(request):
     auth.logout(request)
     return redirect('login')
    

@cache_control(no_cache=True, must_revalidate=True)
def index(request):
 url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=b3fd207c771c1ba1a8b5107f60e87256'
 if request.method=='POST':
    city=request.POST['city'].lower()
 else:
  city = 'jaipur'
 print("hello "+city)
 try:
  city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
  weather = {
  'city' : city,
  'temperature' : city_weather['main']['temp'],
  'description' : city_weather['weather'][0]['description'],
  'icon' : city_weather['weather'][0]['icon']
    }
 except:
  city='jaipur'
  city_weather = requests.get(url.format(city)).json()
 print(city_weather['weather'][0]['icon'])
 weather = {
  'city' : city,
  'temperature' : round(((float(city_weather['main']['temp'])-32)*5)/9,2),
  'max':round(((float(city_weather['main']['temp_max'])-32)*5)/9,2),
  'min':round(((float(city_weather['main']['temp_min'])-32)*5)/9,2),
  'description' : city_weather['weather'][0]['description'],
  'icon' : city_weather['weather'][0]['icon'],
  'humidity':city_weather['main']['humidity'],
  'speed':city_weather['wind']['speed']
    }
 print(weather['icon'])
 context = {'weather' : weather}
 return render(request, 'index.html', weather) #retreturn render(request, 'weat
  
def fetch(c,q):
    url='https://newsapi.org/v2/top-headlines?country=in&sortBy=publishedAt&apiKey=2763db305ddf4e088d8c634d6b821fdd'+q+c+'&pageSize='+str(60)
    req=requests.get(url)
    l=json.loads(req.text)
    # top = newsapi.get_top_headlines(*d)
    l = l['articles']
    desc =[]
    news =[]
    img =[]
    url=[]
    for i in l:
       d=datetime.strptime(i['publishedAt'][:10],'%Y-%m-%d')
       i['day']=d.day
       i['mn']=d.strftime('%B')
    return l



def news(req):
    # if request.method=='GET':
    #  p+=20
    c='&category=sports'
    q=''
    return render(req, 'news.html', context ={"mylist":fetch(c,q)})

def category(req):
    s = req.GET.get('data')
    c='&category='+s
    q=''
    return render(req, 'news.html', context ={"mylist":fetch(c,q)})

def search(req):
    q = req.GET.get('q')
    q='&q='+q
    c=''
    return render(req, 'news.html', context ={"mylist":fetch(c,q)})


def crypto(req):
    return render(req,'crypto.html',{})
  