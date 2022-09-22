from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from rest_framework.test import APIClient
# Create your tests here.
User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
        Tweet.objects.create(content="my first tweet", 
            user=self.user)
        Tweet.objects.create(content="my first tweet", 
            user=self.user)
        Tweet.objects.create(content="my first tweet", 
            user=self.userb)
        self.currentCount = Tweet.objects.all().count()
             
    def test_user_created(self):
        tweet_obj = Tweet.objects.create(content = "my second tweet", user= self.user)   
        self.assertEqual(tweet_obj.id,4)
        self.assertEqual(tweet_obj.user,self.user)
    
    def get_client(self):
         client = APIClient()
         client.login(username = self.user.username, password = "somepassword")
         return client
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/shop/")
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(response.json()),1)

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/shop/")
        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(response.json()),3)  

    def test_tweets_related_name(self):
        user = self.user
        self.assertEqual(user.tweets.count(),2)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/shop/like/", 
            {"id": 1, "action": "like"})
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances_count = user.tweetlike_set.count()
        my_related_likes = user.tweet_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_like_instances_count, my_related_likes)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/shop/like/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/shop/like/", 
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_create_api_view(self):
        request_data = {"content": "this is my test"}
        client = self.get_client()
        response = client.post("/api/shop/create/",request_data )
        self.assertEqual(response.status_code , 201)
        response_data = response.json()
        new_shop_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1,new_shop_id)

    def test_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/shop/1")
        self.assertEqual(response.status_code,200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id,1)
    
    def test_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/shop/1/delete")
        self.assertEqual(response.status_code,200)
        response = client.delete("/api/shop/1/delete")
        self.assertEqual(response.status_code,404)
        response_incorrect_owner = client.delete("/api/shop/3/delete")
        self.assertEqual(response_incorrect_owner.status_code,401)