from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from teamapp.serializers import TeamSerializer
from teamapp.models import Team

# class MemberViewSet(viewsets.ModelViewSet):
#     serializer_class = MemberSerializer
#     queryset = Member.objects.all()


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def create(self, request):
        team_data = request.data
        serializer = TeamSerializer(data=team_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Team.objects.all()
        serializer = TeamSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(queryset, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Team, pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def retrieve(self, request, pk=None):
    #     queryset = get_object_or_404(Team, pk=pk)
    #     serializer = TeamSerializer(queryset)
    #     data = serializer.data
    #     return Response(data)
