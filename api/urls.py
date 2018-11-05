from django.urls import path, include

from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'gender', views.GenderViewSet, base_name='gender')
router.register(r'division', views.DivisionViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'region', views.RegionViewSet)
router.register(r'tag', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
