import random
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings


# Create your views here.
ALLOWED_HOST = settings.ALLOWED_HOSTS

def home(request,*args,**kwargs):
    username = None
    if request.user.is_authenticated:
        username= request.user.username 
    return render(request,"pages/index.html",context={},status=200)

def local_shop_list_view(request,*args,**kwargs):
    return render(request,"shops/list.html")

def local_shop_detail_view(request,tweet_id,*args,**kwargs):
    return render(request,"shops/detail.html",context={"tweetId":tweet_id},status=200)

def local_shop_profile_view(request,username,*args,**kwargs):
    return render(request,"shops/profile.html",context={"profile_username":username})     


