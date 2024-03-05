from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name="create"),
    path('<int:post_id>/', views.detail, name="detail"),
]

#  http://127.0.0.1:8000/blog/posts/?id=1
#  http://127.0.0.1:8000/blog/posts/2/