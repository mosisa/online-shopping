from django.db import models
from django.db.models import Q
import random
from django.conf import settings    

User = settings.AUTH_USER_MODEL
# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    tweet = models.ForeignKey('Tweet',on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True) 

class TweetQuerySet(models.QuerySet):
    def feed(self,user):
        profiles_exists = user.following.exists()
        followed_user_id =[]
        if profiles_exists:
            followed_user_id = user.following.values_list("user_id",flat= True)
        return self.filter(
            Q(user__id__in = followed_user_id)|
            Q( user=user)
            ).distinct().order_by("-timestamp")

class TweetManager(models.Manager):
    def get_querySet(self,*args,**kwargs):
        return TweetQuerySet(self.model,self._db)

    def feed(self,user):
        return self.get_querySet().feed(user) 
        
class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'tweets')
    likes = models.ManyToManyField(User,related_name = 'tweet_user',blank = True,through =TweetLike)
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    class Meta: 
        ordering = ['-id']

    def seralize(self):
        return {
            "id":self.id,
            "content":self.content,
            "likes": random.randint(0,50)
        }