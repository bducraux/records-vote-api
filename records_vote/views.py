from django.db.models import Sum

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Record, VoteCounter
from .serializers import RecordSerializer, VoteCounterSerializer


class RecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows records to be viewed or edited.
    """
    queryset = Record.objects.all().order_by('-created_time')
    serializer_class = RecordSerializer


class VoteCounterList(APIView):
    def get(self, request):
        queryset = VoteCounter.objects.all()
        annotator = self.request.query_params.get('annotator')
        vote = self.request.query_params.get('vote')
        vote_sum = self.request.query_params.get('vote_sum')

        if annotator is not None:
            queryset = queryset.filter(annotator=annotator)
        if vote is not None and vote_sum is None:
            queryset = queryset.filter(vote=vote)
        if vote_sum is not None:
            queryset.filter(vote=vote_sum)
            total = VoteCounter.objects.filter(vote=vote_sum).aggregate(total_sum=Sum('counter'))['total_sum']
            if total is None:
                return Response(f'Vote {vote_sum} is not computed!')

            return Response({'vote': vote_sum, 'total_sum': total})

        queryset= queryset.order_by('annotator', 'vote')

        return Response([{'annotator': item.annotator, 'vote': item.vote, 'count': item.counter} for item in queryset])
