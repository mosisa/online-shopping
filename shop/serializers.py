from rest_framework import serializers
from django.conf import settings
from .models import Tweet
from profiles.serializers import PublicProfileSerializer

MAX_LENGTH = settings.MAX_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self,value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("this is not a valid action for tweets")
        return value
class TweetSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source="user.profile",read_only= True)
    likes = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Tweet
        fields = ["user","id","content","likes","timestamp"]

    def get_likes(self,obj):
        return obj.likes.count()

    # def get_user(self,obj):
    #     return obj.user.id  
            
    def validate_content(self,value):
         if len(value)>MAX_LENGTH:
            raise serializers.ValidationError("this is too long")
         return value      
