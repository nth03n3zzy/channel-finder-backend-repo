from django.shortcuts import render
from rest_framework.views import APIView
from .models import Schedule
from rest_framework.response import Response
from .searlizer import ReactSerializer

# Create your views here.


class NFLTeamScheduleView(APIView):
    serializer_class = ReactSerializer

    def get(self, request, team_name):
        # have a query parameter "team" in the request URL
        print("request recieved")
        team = team_name.lower()

        games = Schedule.objects.filter(team=team)

        serializer = self.serializer_class(games, many=True)

        # Debug: Print the serialized data to the console
        print("Serialized Data:", serializer.data)

        return Response(serializer.data)
