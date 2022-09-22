from django.urls import path
from .views import (
    shop_detail_view,shop_list_veiw,
    tweet_create_view,shop_delete_view,
    shop_like_view,shop_feed_veiw
)

urlpatterns = [
    path('', shop_list_veiw),
    path('feed/', shop_feed_veiw),
    path('like/', shop_like_view),
    path('create/', tweet_create_view),
    path('<int:tweet_id>', shop_detail_view), 
    path('<int:tweet_id>/delete', shop_delete_view),
]   