from rest_framework import serializers
from crud.models import Crud
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    crud = serializers.PrimaryKeyRelatedField(many=True, queryset=Crud.objects.all())

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'crud']


class CrudSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crud
        owner = serializers.ReadOnlyField(source='owner.username')
        highlight = serializers.HyperlinkedIdentityField(view_name='crud-highlight', format='html')
        fields = ['url', 'id', 'title', 'code', 'linenos', 'language', 'style','owner']
    def create(self, validated_data):
        return Crud.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
