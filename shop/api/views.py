import random
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ..models import Tweet
from ..form import TweetForm
from ..serializers import TweetSerializer,TweetActionSerializer

# Create your views here.
ALLOWED_HOST = settings.ALLOWED_HOSTS

  

@api_view(['GET'])
def shop_detail_view(request,tweet_id,*args,**kwargs):
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first()    
    serializer = TweetSerializer(obj)
    return Response(serializer.data,status = 200)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def shop_delete_view(request,tweet_id,*args,**kwargs):
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"you can not delete this tweet"},status=401)
    obj = qs.first()    
    obj.delete()
    return Response({"message":"tweet deleted"},status = 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shop_like_view(request,*args,**kwargs):
    serializer = TweetActionSerializer(data =request.data)
    if serializer.is_valid(raise_exception = True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action  = data.get("action")
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first() 
    if action == "like":
        obj.likes.add(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data,status = 200)  
    elif action == "unlike":
        obj.likes.remove(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data,status = 200)  
    elif action == "retweet":    
        pass  
    return Response({},status = 200)

@api_view(['GET'])
def shop_list_veiw(request,*args,**kwargs):
    qs=Tweet.objects.all()
    username = request.GET.get("username")
    if(username != None):
        qs = qs.filter(user__username__iexact=username)
    return  get_paginated_pages(qs,request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request,*args,**kwargs):
      serializer = TweetSerializer(data=request.data)
      if serializer.is_valid(raise_exception = True):
        serializer.save(user = request.user)
        return Response(serializer.data,status = 201)
      return Response({},status = 400)

def get_paginated_pages(qs,request):
    paginator = PageNumberPagination()
    paginator.page_size= 20
    paginated_qs = paginator.paginate_queryset(qs,request)
    serializer = TweetSerializer(paginated_qs, many =True)
    return  paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shop_feed_veiw(request,*args,**kwargs):
    user = request.user
    qs =Tweet.objects.feed(user)
    return  get_paginated_pages(qs,request)#Response(serializer.data,status = 200)








def tweet_create_view_pure_django(request,*args,**kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax:
            return JsonResponse({},status  = 401)      
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    nexturl = request.POST.get("next")
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user 
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.seralize(),status=201)
        if nexturl!=None and is_safe_url(nexturl,ALLOWED_HOST):
            return redirect(nexturl)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors,status=400)                
    return render(request,'components/form.html',context={"form":form})

def shop_detail_view_pure_dgango(request,tweet_id,*args,**kwargs):
    data ={
        "id": tweet_id,   
    }
    status=200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content']=obj.content
    except:
        data['message']="not found"
        status=404
    
    return JsonResponse(data,status=status)


def shop_list_veiw_pure_djando(request,*args,**kwargs):
    qs=Tweet.objects.all()
    tweets_list=[x.seralize() for x in qs]
    data={
        "response":tweets_list
    }
    return JsonResponse(data)
