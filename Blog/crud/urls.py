from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from crud import views
from crud.views import CrudViewSet, UserViewSet, api_root
from rest_framework import renderers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crud import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'crud', views.CrudViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]


crud_list = CrudViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
crud_detail = CrudViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
crud_highlight = CrudViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('crud/', crud_list, name='crud-list'),
    path('crud/<int:pk>/', crud_detail, name='crud-detail'),
    path('crud/<int:pk>/highlight/', crud_highlight, name='crud-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])


# API endpoints
