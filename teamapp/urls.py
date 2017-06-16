from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from teamapp.views import TeamViewSet

router = routers.DefaultRouter()
router.register(r'team', TeamViewSet, 'team')

urlpatterns = [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^', include(router.urls, namespace='api')),
]
