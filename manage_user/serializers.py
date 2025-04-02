from .models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'city', 'address', 'password', 'password2']

    def validate(self, attrs):
        """
        Vérifie si les mots de passe correspondent avant de créer l'utilisateur.
        """
        if attrs['password'] != attrs.get('password2', ''):
            raise serializers.ValidationError({"password2": _("Les mots de passe ne correspondent pas.")})

        return attrs

    def create(self, validated_data):
        """
        Supprime `password2`, hache le mot de passe et crée l'utilisateur.
        """
        validated_data.pop('password2')  # On enlève le champ inutile
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data['phone_number'],
            city=validated_data['city'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])  # Hash du mot de passe
        user.save()
        return user
