from django.shortcuts import render, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from rest_framework import status
from rest_framework.response import Response
from api.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from payments.models import PaymentMethod
from .models import (
    FoodItem,
    FoodCategory,
    Order,
    OrderItem,
    Table,
    Vat,
    Tax,
    DrinkItem,
    Payment,
    CanclePayment,
)
from .serializers import (
    FoodCategorySerializer,
    FoodItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
    TableSerializer,
    VatSerializer,
    TaxSerializer,
    PaymentSerializer,
)
from inventory.models import DrinksPurchase
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import json


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
    categoryitems = FoodCategory.objects.all()
    categoryitems_serializer = FoodCategorySerializer(categoryitems, many=True)
    return Response(
        {"menu": food_serializer.data, "categories": categoryitems_serializer.data}
    )


@api_view(["GET"])
def categorylists(request):
    categoryitems = FoodCategory.objects.all()
    categoryitems_serializer = FoodCategorySerializer(categoryitems, many=True)
    return Response(categoryitems_serializer.data)


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
    orders = Order.objects.filter(status="Order Placed")
    ordersserializer = OrderSerializer(orders, many=True)
    subtotal = []
    for order in orders:
        subtotal.append(order.ordertotal())
    return Response({"orderdata": ordersserializer.data, "subtotal": subtotal})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orderslists_report(request):
    orders = Order.objects.filter(status="Order Paid")
    ordersserializer = OrderSerializer(orders, many=True)
    subtotal = []
    for order in orders:
        subtotal.append(order.ordertotal())
    return Response({"orderdata": ordersserializer.data, "subtotal": subtotal})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def paymentlists_report(request):
    orders = Payment.objects.filter(status="Paid")
    ordersserializer = PaymentSerializer(orders, many=True)
    return Response(ordersserializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def paymentorderlists(request):
    okayy = []
    userr = User.objects.get(id=request.user.id)
    tabless = Table.objects.all()
    for table in tabless:
        ordee = Order.objects.filter(status="Order Completed", table=table)
        if ordee:
            ordersserializer = OrderSerializer(ordee, many=True)
            okayy.append(ordersserializer.data)

    return Response(okayy)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def completeorder(request, id):
    orders = Order.objects.get(id=int(id))
    orders.status = "Order Completed"
    orders.save()
    return JsonResponse(
        {"success": "Order Completion Successfull"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancleorder(request, id):
    datas = JSONParser().parse(request)
    orders = Order.objects.get(id=int(id))
    orders.status = "Order Canceled"
    if datas:
        orders.cancle_reason = datas["cancel_reason"]
    orders.save()
    return JsonResponse(
        {"success": "Order Canceled Successfull"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancleapyment(request, id):
    datas = JSONParser().parse(request)
    tablee = Table.objects.get(id=id)
    iddd = request.user.id
    usss = User.objects.get(id=iddd)
    ordee = Order.objects.filter(table=tablee)
    for ord in ordee:
        ord.status = "Order Canceled"
        ord.save()
    payme = CanclePayment.objects.create(user=usss, status="Unpaid", table=tablee)
    payme.order.set(ordee)
    if datas:
        payme.cancle_reason = datas["cancel_reason"]
    payme.save()
    return JsonResponse(
        {"success": "Payment Canceled Successfull"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submitcart(request):
    try:
        datas = JSONParser().parse(request)
        userr = User.objects.get(id=request.user.id)
        tabb = Table.objects.get(table_name=datas["table"])
        ordee = Order.objects.create(
            user=userr, order_note=datas["ordernote"], table=tabb
        )
        for data in datas["cartt"]:
            foodi = FoodItem.objects.get(id=data["item"]["id"])
            newobj = OrderItem.objects.create(
                user=userr, food_item=foodi, no_of_items=data["qty"]
            )
            if foodi.is_a_drink:
                drinkkk = DrinkItem.objects.get(name=foodi.name)
                """ newobj.drink_quantity = data["drink_quantity"]
                newobj.save() """
                try:
                    dp = DrinksPurchase.objects.get(drinkk=drinkkk)
                    dp.quantity -= int(data["drink_quantity"])
                    dp.save()
                except:
                    pass

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
        tablee = Table.objects.get(table_name=datas["table_name"])
        paymentmethod = PaymentMethod.objects.get(
            payment_method_name=datas["payment_method"]
        )
        ordee = Order.objects.filter(table=tablee)
        for ord in ordee:
            ord.status = "Order Paid"
            ord.save()
        payme = Payment.objects.create(
            order=ordee, payment_method=paymentmethod, status="Paid", table=tablee
        )
        if paymentmethod.payment_method_name == "Card":
            payme.bank_name = datas["bank_name"]
        payme.save()

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


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addTable(request):
    try:
        datas = JSONParser().parse(request)
        table = Table.objects.create(table_name=datas["table_name"])
        table.save()

        return JsonResponse(
            {"success": "Table Created Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Table Addition Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singleTable(request, id):
    try:
        table = Table.objects.get(id=id)
        table_serializer = TableSerializer(table)
        return Response(table_serializer.data)
    except:
        return JsonResponse(
            {"error": "Invalid Table"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateTable(request):
    try:
        datas = JSONParser().parse(request)
        table = Table.objects.get(id=datas["id"])
        table.table_name = datas["table_name"]
        table.save()
        return JsonResponse(
            {"success": "Table Updated Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Table Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteTable(request):
    try:
        datas = JSONParser().parse(request)
        table = Table.objects.get(id=datas["id"])
        table.delete()

        return JsonResponse(
            {"success": "Table Delete Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Table Delete Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def vatandtaxlists(request):
    vats = Vat.objects.all()
    taxes = Tax.objects.all()
    vats_serializer = VatSerializer(vats, many=True)
    taxess_serializer = TaxSerializer(taxes, many=True)
    return Response({"vats": vats_serializer.data, "taxes": taxess_serializer.data})


@api_view(["GET"])
def vatlists(request):
    vats = Vat.objects.all()
    vats_serializer = VatSerializer(vats, many=True)
    return Response(vats_serializer.data)


@api_view(["GET"])
def taxlists(request):
    taxes = Tax.objects.all()
    taxess_serializer = TaxSerializer(taxes, many=True)
    return Response(taxess_serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addVat(request):
    try:
        datas = JSONParser().parse(request)
        vat = Vat.objects.create(
            vat_name=datas["vat_name"], vat_percentage=datas["vat_percentage"]
        )
        vat.save()

        return JsonResponse(
            {"success": "Vat Created Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Vat Addition Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singleVat(request, id):
    try:
        vat = Vat.objects.get(id=id)
        vat_serializer = VatSerializer(vat)
        return Response(vat_serializer.data)
    except:
        return JsonResponse(
            {"error": "Invalid Vat"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateVat(request):
    try:
        datas = JSONParser().parse(request)
        vat = Vat.objects.get(id=datas["id"])
        vat.vat_name = datas["vat_name"]
        vat.vat_percentage = datas["vat_percentage"]
        vat.save()
        return JsonResponse(
            {"success": "Vat Updated Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Vat Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteVat(request):
    try:
        datas = JSONParser().parse(request)
        vat = Vat.objects.get(id=datas["id"])
        vat.delete()

        return JsonResponse(
            {"success": "Vat Delete Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Vat Delete Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addTax(request):
    try:
        datas = JSONParser().parse(request)
        tax = Tax.objects.create(
            tax_name=datas["tax_name"], tax_percentage=datas["tax_percentage"]
        )
        tax.save()

        return JsonResponse(
            {"success": "Tax Created Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Tax Addition Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singleTax(request, id):
    try:
        tax = Tax.objects.get(id=id)
        tax_serializer = TaxSerializer(tax)
        return Response(tax_serializer.data)
    except:
        return JsonResponse(
            {"error": "Invalid Tax"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateTax(request):
    try:
        datas = JSONParser().parse(request)
        tax = Tax.objects.get(id=datas["id"])
        tax.tax_name = datas["tax_name"]
        tax.tax_percentage = datas["tax_percentage"]
        tax.save()
        return JsonResponse(
            {"success": "Tax Updated Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Tax Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteTax(request):
    try:
        datas = JSONParser().parse(request)
        tax = Tax.objects.get(id=datas["id"])
        tax.delete()

        return JsonResponse(
            {"success": "Tax Delete Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Tax Delete Failed"}, status=status.HTTP_400_BAD_REQUEST
        )
