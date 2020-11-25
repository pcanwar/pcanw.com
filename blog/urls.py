from django.urls import path

from .feeds import LatestPostsFeed
from .views import post_api_details, post_api_list, post_detail,post_list,post_search, about
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('employs', )



app_name = 'blog'
urlpatterns = [

    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),

    path('<uuid:uuid>/',  post_detail, name='post_detail'),

    path('feed/', LatestPostsFeed(), name='post_feed'),

    path('search/', post_search, name='post_search'),
    path('about/', about, name='about'),


    #     api
    path('api/', post_api_list),
    path('api/<uuid:uuid>/', post_api_details),

    #     router
    # path('', include(router.urls)),

]
