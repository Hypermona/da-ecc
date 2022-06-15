from urllib import response
from django.http import JsonResponse
# from .models import Survey
# from .serializers import SurveySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .data_aggr import data_agg


@api_view(['GET', "POST"])
def drink_list(requet):

    if requet.method == "POST":
        print(type(requet.data))
        data = data_agg(data=requet.data)

        return Response({"charts": data["charts"], "encryption": data["enc"], "decryption": data["dec"]})
        # survey = Survey.objects.all()
        # ss = SurveySerializer(survey, many=True)
        # return JsonResponse({"surveys": ss.data})

    # if requet.method == "POST":
    #     ss = SurveySerializer(data=requet.data)
    #     if ss.is_valid():
    #         ss.save()
    #         return Response(ss.data, status=status.HTTP_201_CREATED)
