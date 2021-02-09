from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from rest_framework import routers
from levelupapi.views import gametype, game


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', gametype, 'gametype')
router.register(r'games', game, 'game')

urlpatterns = [
    # Requests to http://localhost:8088/register will be routed to the register_user function
    path('register', register_user),
    # Requests to http://localhost:8088/login will be routed the login_user function
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]