from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .views import MemberViewSet

router = routers.DefaultRouter()
router.register(r'member', MemberViewSet, 'member')

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/token-auth/', obtain_jwt_token),
]
