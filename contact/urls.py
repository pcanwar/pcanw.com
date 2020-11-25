from django.urls import path

from .views import contactView, successView, resumeView

app_name = 'contact'

urlpatterns = [
    path('', contactView, name='contact'),
    path('success/', successView, name='success'),
    path('resume/', resumeView, name='resume'),

]