from rest_framework import serializers
from app.models import Client, Series, Comic, Subscription
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "client_number",
            "first_name",
            "last_name",
            "birthdate",
            "registration_date",
            "address",
            "email_address",
        ]


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = [
            "publisher",
            "name",
            "volume",
        ]


class ComicSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(many=False, read_only=True)

    class Meta:
        model = Comic
        fields = ["series", "issue", "pub_date", "price", "writer", "penciller"]


class SubscriptionSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True)
    series = SeriesSerializer(many=False, read_only=True)

    class Meta:
        model = Subscription
        fields = ["client", "series", "begin_date", "end_date"]


"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=400)

    def create(self, validated_data):
        return Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
"""
