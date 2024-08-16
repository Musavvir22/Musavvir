from django.urls import path,include
from .views import PersonAPI,PersonViewSet
from .import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'viewset', PersonViewSet, basename='tahir')   # viewset urls 
urlpatterns = router.urls



urlpatterns = [
    path('',include(router.urls)), # viewset urls 
    path('api/',views.index,name="index"),
    # path('person/',views.person),
    path('login/',views.login),
    path('PersonsAPI/',PersonAPI.as_view())

]
