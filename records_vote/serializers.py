from .models import Record, VoteCounter
from rest_framework import serializers


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['votes', 'created_time']


class VoteCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteCounter
        fields = ['annotator', 'vote', 'counter']
