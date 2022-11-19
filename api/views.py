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
from .models import FoodItem, FoodCategory, Order, OrderItem,Table
from .serializers import (
    FoodCategorySerializer,
    FoodItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
    TableSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "user_type": user.user_type,
            }
        )


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
def tablelists(request):
    tables = Table.objects.all()
    tables_serializer = TableSerializer(tables, many=True)
    return Response(tables_serializer.data)


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
        ordee = Order.objects.filter(payment_status="Unpaid")
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
        sorting = request.GET.get("sorting", 1)

        if category == "All":
            if sorting == "1":
                foods = FoodItem.objects.all().order_by("price")
            else:
                foods = FoodItem.objects.all().order_by("-price")
        else:
            foodcats = FoodCategory.objects.get(name=category)
            if sorting == "1":
                foods = FoodItem.objects.filter(category=foodcats).order_by("price")
            else:
                foods = FoodItem.objects.filter(category=foodcats).order_by("-price")

        foodser = FoodItemSerializer(foods, many=True)
        return Response(foodser.data)
