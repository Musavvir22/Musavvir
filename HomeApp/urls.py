from django.urls import path,include
from .views import PersonAPI,PersonViewSet,RegisterAPI,LoginAPI
from .import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'viewset', PersonViewSet, basename='viewset')   # viewset urls 
urlpatterns = router.urls



urlpatterns = [
    path('',include(router.urls)), # viewset urls 
    path('register/',RegisterAPI.as_view()),
    path('loginapi/',LoginAPI.as_view()),
    path('api/',views.index,name="index"),
    # path('person/',views.person),
    path('login/',views.login),
    path('PersonsAPI/',PersonAPI.as_view())

]
