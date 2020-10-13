from crud.models import Crud
from crud.serializers import CrudSerializer
from rest_framework import mixins
from rest_framework import generics
from crud.models import Crud
from crud.serializers import CrudSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from crud.serializers import UserSerializer
from rest_framework import permissions
from crud.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from crud.models import Crud
from crud.serializers import CrudSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class CrudViewSet(viewsets.ModelViewSet):

    queryset = Crud.objects.all()
    serializer_class = CrudSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        crud = self.get_object()
        return Response(crud.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'crud': reverse('crud-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def crud_list(request):

    if request.method == 'GET':
        crud = Crud.objects.all()
        serializer = CrudSerializer(crud, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CrudSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def crud_detail(request, pk):
    """
    Retrieve, update or delete a code crud.
    """
    try:
        crud = Crud.objects.get(pk=pk)
    except Crud.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrudSerializer(crud)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CrudSerializer(crud, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        crud.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
