from django.shortcuts import render, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .models import FoodItem, FoodCategory, Order, OrderItem, Advertisement
from .serializers import (
    AdvertisementSerializer,
    FoodCategorySerializer,
    FoodItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
)


@api_view(["GET"])
def ads(request):
    aditems = Advertisement.objects.all()
    ad_serializer = AdvertisementSerializer(aditems, many=True)
    return Response(ad_serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def foodlists(request):
    fooditems = FoodItem.objects.all()
    food_serializer = FoodItemSerializer(fooditems, many=True)
    return Response(food_serializer.data)


@api_view(["GET"])
def categorylists(request):
    fooditems = FoodCategory.objects.all()
    food_serializer = FoodCategorySerializer(fooditems, many=True)
    return Response(food_serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orderslists(request):
    userr = User.objects.get(id=request.user.id)
    orders = Order.objects.filter(user=userr)
    ordersserializer = OrderSerializer(orders, many=True)
    subtotal = 0
    for order in orders:
        subtotal += order.ordertotal()
    return Response({"orderdata": ordersserializer.data, "subtotal": subtotal})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submitcart(request):
    try:
        datas = JSONParser().parse(request)
        userr = User.objects.get(id=request.user.id)
        ordee = Order.objects.create(user=userr, order_note="No Order note")
        for data in datas:
            foodi = FoodItem.objects.get(id=data["item"]["id"])
            newobj = OrderItem.objects.create(
                user=userr, food_item=foodi, no_of_items=data["qty"]
            )
            ordee.orderitems.add(newobj)

        ordee.save()
        return JsonResponse(
            {"success": "Order Submission Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Order Submission Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def paymentt(request):
    try:
        datas = JSONParser().parse(request)
        userr = User.objects.get(id=request.user.id)
        ordee = Order.objects.all()
        for data in ordee:
            data.payment_method = datas["paymentmethod"]
            data.payment_status = "Verifying"
            data.save()

        return JsonResponse(
            {"success": "Payment Submission Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Order Payment Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def foodlists_search(request):
    if request.method == "GET":
        category = request.GET.get("category", "All")
        pricemin = request.GET.get("min", 0)
        pricemax = request.GET.get("max", 0)
        if pricemax == "":
            pricemax = "0"
        if pricemin == "":
            pricemin = "0"
        if category == "All":
            if pricemax == "0":
                foods = FoodItem.objects.filter(price__gte=int(pricemin))
            else:
                foods = FoodItem.objects.filter(
                    price__gte=int(pricemin), price__lte=int(pricemax)
                )
        else:
            foodcats = FoodCategory.objects.get(name=category)
            if pricemax == "0":
                foods = FoodItem.objects.filter(
                    category=foodcats, price__gte=int(pricemin)
                )
            else:
                foods = FoodItem.objects.filter(
                    category=foodcats,
                    price__gte=int(pricemin),
                    price__lte=int(pricemax),
                )

        foodser = FoodItemSerializer(foods, many=True)
        return Response(foodser.data)
