from rest_framework import serializers
from .models import Offer
from django.conf import settings


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'offerDate', 'context', 'field_O', 'fileOffer', 'mode',
                  'owner')
def create(self, validated_data):
        instance = Offer.objects.create(**validated_data)
        return instance

