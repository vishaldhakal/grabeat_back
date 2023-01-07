from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status
from .models import DrinksPurchase


""" def uploadDrinkPurchases(request):
    filee = request.FILES["csvfile"]
    file_data = filee.read().decode("utf-8")
    lines = file_data.split("\n")

    for line in lines:
          supplier = 
          okk = DrinksPurchase.objects.create(imei_no=line)
          okk.save()

    return JsonResponse(
        {"success": "Drink Purchase Upload Successfull"},
        status=status.HTTP_201_CREATED,
    )
 """
