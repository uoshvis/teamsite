from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import MemberSerializer
from .models import Member


class MemberViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving members.
    """
    model = Member
    # queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def list(self, request):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)
