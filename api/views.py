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
from rest_framework.pagination import PageNumberPagination
from payments.models import PaymentMethod, Bank
from inventory.models import Expenses
from inventory.serializers import ExpensesSerializer
from payments.serializers import PaymentMethodSerializer, BankSerializer
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
    FoodItemSmallSerializer,
    PaymentSmallSerializer,
)
from inventory.serializers import (
    DrinkPurchaseSerializer,
    PurchaseSerializer,
    DrinkStockSerializer,
)
from accounts.serializers import UserSerializer
from inventory.models import DrinksPurchase, Purchase, DrinksStock
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import json
import math
from datetime import date, datetime, timedelta


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
def foodlists(request):
    queryy = request.GET.get("query", "All")
    fooditems = FoodItem.objects.all()
    if queryy != "All":
        fooditems = FoodItem.objects.filter(name__contains=queryy).order_by("-name")

    food_serializer = FoodItemSerializer(fooditems, many=True)
    food_serializer2 = FoodItemSmallSerializer(fooditems, many=True)
    categoryitems = FoodCategory.objects.all().order_by("-name")
    categoryitems_serializer = FoodCategorySerializer(categoryitems, many=True)
    return Response(
        {
            "menu": food_serializer.data,
            "categories": categoryitems_serializer.data,
            "menulists": food_serializer2.data,
        }
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
def orderslists(request):

    table = request.GET.get("table", "All")
    waiter = request.GET.get("waiter", "All")
    orders = []

    if (table == "All") & (waiter == "All"):
        orders = Order.objects.filter(status="Order Placed")
    elif (table == "All") & (waiter != "All"):
        usss = User.objects.get(username=waiter)
        orders = Order.objects.filter(status="Order Placed", user=usss)
    elif (table != "All") & (waiter == "All"):
        table = Table.objects.get(table_name=table)
        orders = Order.objects.filter(status="Order Placed", table=table)
    else:
        usss = User.objects.get(username=waiter)
        table = Table.objects.get(table_name=table)
        orders = Order.objects.filter(status="Order Placed", table=table, user=usss)

    userss = User.objects.all()
    userss_serializer = UserSerializer(userss, many=True)
    tabless = Table.objects.all()
    tabless_serializer = TableSerializer(tabless, many=True)
    ordersserializer = OrderSerializer(orders, many=True)
    subtotal = []

    for order in orders:
        subtotal.append(order.ordertotal())
    return Response(
        {
            "orderdata": ordersserializer.data,
            "subtotal": subtotal,
            "users": userss_serializer.data,
            "tables": tabless_serializer.data,
        }
    )


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data, noo):
        return Response(
            {
                "totalCount": self.page.paginator.count,
                "totalPages": noo,
                "dataPerpage": self.page_size,
                "results": data,
            }
        )


@api_view(["GET"])
def all_report(request):
    paginationsize = request.GET.get("perpage", "10")

    payments = Payment.objects.filter(status="Paid")

    drinkspurchase = DrinksPurchase.objects.all()

    purchases = Purchase.objects.all()

    drinkorders = OrderItem.objects.filter(food_item__is_a_drink=True)
    drinkorders_serializer = OrderItemSerializer(drinkorders, many=True)

    drinkstocks = DrinksStock.objects.all()
    drinkstocks_serializer = DrinkStockSerializer(drinkstocks, many=True)

    allexps = Expenses.objects.all()
    allexps_serializer = ExpensesSerializer(allexps, many=True)

    paginator = CustomPagination()
    paginator.page_size = int(paginationsize)
    total_data1 = payments.count()
    total_data2 = drinkspurchase.count()
    total_data3 = purchases.count()
    total_data4 = drinkorders.count()
    total_data5 = allexps.count()

    no_of_pages1 = math.ceil(total_data1 / paginator.page_size)
    no_of_pages2 = math.ceil(total_data2 / paginator.page_size)
    no_of_pages3 = math.ceil(total_data3 / paginator.page_size)
    no_of_pages4 = math.ceil(total_data4 / paginator.page_size)
    no_of_pages5 = math.ceil(total_data5 / paginator.page_size)

    result_page1 = paginator.paginate_queryset(payments, request)
    result_page2 = paginator.paginate_queryset(drinkspurchase, request)
    result_page3 = paginator.paginate_queryset(purchases, request)
    result_page4 = paginator.paginate_queryset(drinkorders, request)
    result_page5 = paginator.paginate_queryset(allexps, request)

    payments_serializer = PaymentSmallSerializer(result_page1, many=True)
    drinkspurchase_serializer = DrinkPurchaseSerializer(result_page2, many=True)
    purchases_serializer = PurchaseSerializer(result_page3, many=True)
    drinkorders_serializer = OrderItemSerializer(result_page4, many=True)
    allexps_serializer = ExpensesSerializer(result_page5, many=True)

    final1 = paginator.get_paginated_response(payments_serializer.data, no_of_pages1)
    final2 = paginator.get_paginated_response(
        drinkspurchase_serializer.data, no_of_pages2
    )
    final3 = paginator.get_paginated_response(purchases_serializer.data, no_of_pages3)
    final4 = paginator.get_paginated_response(drinkorders_serializer.data, no_of_pages4)
    final5 = paginator.get_paginated_response(allexps_serializer.data, no_of_pages5)

    return Response(
        {
            "payments": final1.data,
            "drinks_purchase": final2.data,
            "purchase": final3.data,
            "expenses": final5.data,
            "drinkorders": final4.data,
            "drinkstocks": drinkstocks_serializer.data,
        }
    )


@api_view(["GET"])
def misc_expense_report(request):
    paginationsize = request.GET.get("perpage", "10")
    allexps = Expenses.objects.all()

    paginator = CustomPagination()
    paginator.page_size = int(paginationsize)
    total_data = allexps.count()
    no_of_pages = math.ceil(total_data / paginator.page_size)
    result_page = paginator.paginate_queryset(allexps, request)
    serializer_cat = ExpensesSerializer(result_page, many=True)
    final = paginator.get_paginated_response(serializer_cat.data, no_of_pages)

    return Response(
        {
            "expenses": final.data,
        }
    )


@api_view(["GET"])
def paymentss_report(request):
    """paginationsize = request.GET.get("perpage", "10")"""
    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    start_date = request.GET.get("start_date", today)
    end_date = request.GET.get("end_date", tomorrow)

    payments = Payment.objects.filter(
        status="Paid", created__gte=start_date, created__lte=end_date
    ).order_by("-created")

    """ paginator = CustomPagination()
    paginator.page_size = int(paginationsize)
    total_data = payments.count()
    no_of_pages = math.ceil(total_data / paginator.page_size)
    result_page = paginator.paginate_queryset(payments, request)
    final = paginator.get_paginated_response(serializer_cat.data, no_of_pages) """
    serializer_cat = PaymentSmallSerializer(payments, many=True)

    return Response(
        {
            "payments": serializer_cat.data,
        }
    )


@api_view(["GET"])
def purchases_report(request):

    paginationsize = request.GET.get("perpage", "10")
    purchases = Purchase.objects.all()

    paginator = CustomPagination()
    paginator.page_size = int(paginationsize)
    total_data = purchases.count()
    no_of_pages = math.ceil(total_data / paginator.page_size)
    result_page = paginator.paginate_queryset(purchases, request)
    serializer_cat = PurchaseSerializer(result_page, many=True)
    final = paginator.get_paginated_response(serializer_cat.data, no_of_pages)

    return Response(
        {
            "purchase": final.data,
        }
    )


@api_view(["GET"])
def drink_purchases_report(request):

    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    start_date = request.GET.get("start_date", today)
    end_date = request.GET.get("end_date", tomorrow)

    drinkspurchase = DrinksPurchase.objects.filter(
        date__gte=start_date, date__lte=end_date
    )

    serializer_cat = DrinkPurchaseSerializer(drinkspurchase, many=True)

    return Response(
        {
            "drink_purchase": serializer_cat.data,
        }
    )


@api_view(["GET"])
def drink_orders_report(request):

    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    start_date = request.GET.get("start_date", today)
    end_date = request.GET.get("end_date", tomorrow)
    drinkorders = OrderItem.objects.filter(
        food_item__is_a_drink=True, created__gte=start_date, created__lte=end_date
    )
    serializer_cat = OrderItemSerializer(drinkorders, many=True)

    return Response(
        {
            "drinkorders": serializer_cat.data,
        }
    )


@api_view(["GET"])
def drink_stocks_report(request):

    drinkstocks = DrinksStock.objects.all()
    serializer_cat = DrinkStockSerializer(drinkstocks, many=True)

    return Response(
        {
            "drinkstocks": serializer_cat.data,
        }
    )


@api_view(["GET"])
def drinks_report(request):
    drinkspurchase = DrinksPurchase.objects.all()
    drinkspurchase_serializer = DrinkPurchaseSerializer(drinkspurchase, many=True)

    drinkorders = OrderItem.objects.filter(food_item__is_a_drink=True)
    drinkorders_serializer = OrderItemSerializer(drinkorders, many=True)

    drinkstocks = DrinksStock.objects.all()
    drinkstocks_serializer = DrinkStockSerializer(drinkstocks, many=True)

    return Response(
        {
            "drinks_purchase": drinkspurchase_serializer.data,
            "drinkorders": drinkorders_serializer.data,
            "drinkstocks": drinkstocks_serializer.data,
        }
    )


@api_view(["GET"])
def orderslists_report(request):
    table = request.GET.get("table", "All")
    waiter = request.GET.get("waiter", "All")

    paginationsize = request.GET.get("perpage", "30")

    if (table == "All") & (waiter == "All"):
        orders = Order.objects.filter(status="Order Paid")
    elif (table == "All") & (waiter != "All"):
        usss = User.objects.get(username=waiter)
        orders = Order.objects.filter(status="Order Paid", user=usss)
    elif (table != "All") & (waiter == "All"):
        table = Table.objects.get(table_name=table)
        orders = Order.objects.filter(status="Order Paid", table=table)
    else:
        usss = User.objects.get(username=waiter)
        table = Table.objects.get(table_name=table)
        orders = Order.objects.filter(status="Order Paid", table=table, user=usss)

    paginator = CustomPagination()
    paginator.page_size = int(paginationsize)
    total_data = orders.count()
    no_of_pages = math.ceil(total_data / paginator.page_size)
    result_page = paginator.paginate_queryset(orders, request)
    serializer_cat = OrderSerializer(result_page, many=True)
    final = paginator.get_paginated_response(serializer_cat.data, no_of_pages)

    subtotal = []
    for order in orders:
        subtotal.append(order.ordertotal())

    userss = User.objects.all()
    userss_serializer = UserSerializer(userss, many=True)
    tabless = Table.objects.all()
    tabless_serializer = TableSerializer(tabless, many=True)
    return Response(
        {
            "orderdata": final.data,
            "subtotal": subtotal,
            "users": userss_serializer.data,
            "tables": tabless_serializer.data,
        }
    )


@api_view(["GET"])
def paymentlists_report(request):

    table = request.GET.get("table", "All")
    waiter = request.GET.get("waiter", "All")

    paginationsize = request.GET.get("perpage", "30")

    if (table == "All") & (waiter == "All"):
        orders = Payment.objects.filter(status="Paid")
    elif (table == "All") & (waiter != "All"):
        usss = User.objects.get(username=waiter)
        orders = Payment.objects.filter(status="Paid", user=usss)
    elif (table != "All") & (waiter == "All"):
        table = Table.objects.get(table_name=table)
        orders = Payment.objects.filter(status="Paid", table=table)
    else:
        usss = User.objects.get(username=waiter)
        table = Table.objects.get(table_name=table)
        orders = Payment.objects.filter(status="Paid", user=usss, table=table)

    paginator = CustomPagination()
    paginator.page_size = int(paginationsize)
    total_data = orders.count()
    no_of_pages = math.ceil(total_data / paginator.page_size)
    result_page = paginator.paginate_queryset(orders, request)
    serializer_cat = PaymentSerializer(result_page, many=True)
    final = paginator.get_paginated_response(serializer_cat.data, no_of_pages)

    userss = User.objects.all()
    userss_serializer = UserSerializer(userss, many=True)
    tabless = Table.objects.all()
    tabless_serializer = TableSerializer(tabless, many=True)
    return Response(
        {
            "payments": final.data,
            "users": userss_serializer.data,
            "tables": tabless_serializer.data,
        }
    )


@api_view(["POST"])
def kot_printed(request, id):
    try:
        orders = Order.objects.get(id=id)
        orders.is_kot_printed = True
        orders.save()
        return JsonResponse(
            {"success": "Kot Printed Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Kot Print Error"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def paymentorderlists(request):
    okayy = []

    table = request.GET.get("table", "All")
    waiter = request.GET.get("waiter", "All")

    tabless = Table.objects.all()

    if table == "All":
        tabless = Table.objects.all()
    else:
        tabless = Table.objects.filter(table_name=table)

    for table in tabless:
        if waiter == "All":
            ordee = Order.objects.filter(status="Order Completed", table=table)
        else:
            usss = User.objects.get(username=waiter)
            tabless = Table.objects.get(table_name=table)
            ordee = Order.objects.filter(
                status="Order Completed", table=table, user=usss
            )

        if ordee:
            ordersserializer = OrderSerializer(ordee, many=True)
            okayy.append(ordersserializer.data)

    userss = User.objects.all()
    userss_serializer = UserSerializer(userss, many=True)
    tabless = Table.objects.all()
    tabless_serializer = TableSerializer(tabless, many=True)

    return Response(
        {
            "payments": okayy,
            "users": userss_serializer.data,
            "tables": tabless_serializer.data,
        }
    )


@api_view(["GET"])
def paymentorderlistscredit(request):
    okayy = []

    table = request.GET.get("table", "All")
    waiter = request.GET.get("waiter", "All")

    tabless = Table.objects.all()

    if table == "All":
        tabless = Table.objects.all()
    else:
        tabless = Table.objects.filter(table_name=table)

    for table in tabless:
        if waiter == "All":
            ordee = Order.objects.filter(status="Order Completed", table=table)
        else:
            usss = User.objects.get(username=waiter)
            tabless = Table.objects.get(table_name=table)
            ordee = Order.objects.filter(
                status="Order Completed", table=table, user=usss
            )

        if ordee:
            ordersserializer = OrderSerializer(ordee, many=True)
            okayy.append(ordersserializer.data)

    userss = User.objects.all()
    userss_serializer = UserSerializer(userss, many=True)
    tabless = Table.objects.all()
    tabless_serializer = TableSerializer(tabless, many=True)

    return Response(
        {
            "payments": okayy,
            "users": userss_serializer.data,
            "tables": tabless_serializer.data,
        }
    )


def changecategory(request):

    return JsonResponse(
        {"success": "Category Updated Successfull"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def paymentorderlistsingle(request, id):
    tabless = Table.objects.get(id=id)
    ordee = Order.objects.filter(status="Order Completed", table=tabless)
    ordersserializer = OrderSerializer(ordee, many=True)
    bankss = Bank.objects.all()
    banksserializer = BankSerializer(bankss, many=True)
    pm = PaymentMethod.objects.all()
    pmserializer = PaymentMethodSerializer(pm, many=True)
    latest_idd = Payment.objects.all().order_by("-id")[:1]
    return Response(
        {
            "payment_id": latest_idd[0].id + 1,
            "order": ordersserializer.data,
            "banks": banksserializer.data,
            "payment_methods": pmserializer.data,
        }
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def completeorder(request, id):
    orders = Order.objects.get(id=int(id))
    orders.status = "Order Completed"
    for itemm in orders.orderitems.all():
        itemm.status = "Order Completed"
        itemm.save()
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
    for itemm in orders.orderitems.all():
        itemm.status = "Order Canceled"
        itemm.save()
        if itemm.food_item.is_a_drink:
            foodi = itemm.food_item
            try:
                drinkkk = DrinkItem.objects.get(name=foodi.name)
                dpp = DrinksStock.objects.filter(drinkk=drinkkk)
                dp = dpp[0]
                if foodi.drink_metric == "Ml":
                    calc = dp.quantity
                    calc += int(itemm.no_of_items) * foodi.drink_quantity
                    dp.quantity = calc
                elif foodi.drink_metric == "Qtr":
                    calc = dp.quantity
                    calc += int(itemm.no_of_items) * 180
                    dp.quantity = calc
                elif foodi.drink_metric == "Half":
                    calc = dp.quantity
                    calc += int(itemm.no_of_items) * 350
                    dp.quantity = calc
                elif foodi.drink_metric == "Full":
                    calc = dp.quantity
                    calc += int(itemm.no_of_items) * 750
                    dp.quantity = calc
                elif foodi.drink_metric == "Beer Bottle Small":
                    calc = dp.quantity
                    calc += int(itemm.no_of_items) * 1
                    dp.quantity = calc
                else:
                    if foodi.drink_metric == "Glass":
                        if foodi.type_of_drink == "Beer":
                            calc = dp.quantity
                            calc += int(itemm.no_of_items) * foodi.drink_quantity * 0.5
                            dp.quantity = calc
                        elif foodi.type_of_drink == "Wine":
                            calc = dp.quantity
                            calc += int(itemm.no_of_items) * 150
                            dp.quantity = calc
                        else:
                            calc = dp.quantity
                            calc += int(itemm.no_of_items) * foodi.drink_quantity
                            dp.quantity = calc
                    else:
                        if foodi.type_of_drink == "Wine":
                            calc = dp.quantity
                            calc += int(itemm.no_of_items) * 1000
                            dp.quantity = calc
                        else:
                            calc = dp.quantity
                            calc += int(itemm.no_of_items) * foodi.drink_quantity
                            dp.quantity = calc
                dp.save()
            except:
                pass
        else:
            pass

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
def cancleorderitem(request, id):
    itemm = OrderItem.objects.get(id=int(id))
    orderss = itemm.orderitems.all()
    aaa = orderss[0]
    itemm.status = "Order Canceled"
    aaa.orderitems.remove(itemm)
    aaa.save()
    itemm.save()
    if itemm.food_item.is_a_drink:
        foodi = itemm.food_item
        try:
            drinkkk = DrinkItem.objects.get(name=foodi.name)
            dpp = DrinksStock.objects.filter(drinkk=drinkkk)
            dp = dpp[0]
            if foodi.drink_metric == "Ml":
                calc = dp.quantity
                calc += int(itemm.no_of_items) * foodi.drink_quantity
                dp.quantity = calc
            elif foodi.drink_metric == "Qtr":
                calc = dp.quantity
                calc += int(itemm.no_of_items) * 180
                dp.quantity = calc
            elif foodi.drink_metric == "Half":
                calc = dp.quantity
                calc += int(itemm.no_of_items) * 350
                dp.quantity = calc
            elif foodi.drink_metric == "Full":
                calc = dp.quantity
                calc += int(itemm.no_of_items) * 750
                dp.quantity = calc
            elif foodi.drink_metric == "Beer Bottle Small":
                calc = dp.quantity
                calc += int(itemm.no_of_items) * 1
                dp.quantity = calc
            else:
                if foodi.drink_metric == "Glass":
                    if foodi.type_of_drink == "Beer":
                        calc = dp.quantity
                        calc += int(itemm.no_of_items) * foodi.drink_quantity * 0.5
                        dp.quantity = calc
                    elif foodi.type_of_drink == "Wine":
                        calc = dp.quantity
                        calc += int(itemm.no_of_items) * 150
                        dp.quantity = calc
                    else:
                        calc = dp.quantity
                        calc += int(itemm.no_of_items) * foodi.drink_quantity
                        dp.quantity = calc
                else:
                    if foodi.type_of_drink == "Wine":
                        calc = dp.quantity
                        calc += int(itemm.no_of_items) * 1000
                        dp.quantity = calc
                    else:
                        calc = dp.quantity
                        calc += int(itemm.no_of_items) * foodi.drink_quantity
                        dp.quantity = calc
            dp.save()
        except:
            pass
    else:
        pass

    if aaa.orderitems.count() == 0:
        aaa.status = "Order Canceled"
        aaa.save()
    return JsonResponse(
        {"success": "Order Item Canceled Successfull"},
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
        for itemm in ord.orderitems.all():
            itemm.status = "Payment Canceled"
            itemm.save()

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
        idd = request.user.id
        userr = User.objects.get(id=idd)
        tabb = Table.objects.get(table_name=datas["table"])
        if datas["ordernote"]:
            ordee = Order.objects.create(
                user=userr, order_note=datas["ordernote"], table=tabb
            )
        else:
            ordee = Order.objects.create(
                user=userr, order_note="No order note", table=tabb
            )
        for data in datas["cartt"]:
            foodi = FoodItem.objects.get(id=data["item"]["id"])
            if foodi.is_a_drink:
                try:
                    drinkkk = DrinkItem.objects.get(name=foodi.name)
                    dpp = DrinksStock.objects.filter(drinkk=drinkkk)
                    dp = dpp[0]
                    if foodi.drink_metric == "Ml":
                        calc = dp.quantity
                        if (int(data["qty"]) * foodi.drink_quantity) > calc:
                            ordee.delete()
                            return JsonResponse(
                                {"error": foodi.name + " Not Available in Inventory"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
                        calc -= int(data["qty"]) * foodi.drink_quantity
                        dp.quantity = calc
                    elif foodi.drink_metric == "Qtr":
                        calc = dp.quantity
                        if (int(data["qty"]) * 180) > calc:
                            ordee.delete()
                            return JsonResponse(
                                {"error": foodi.name + " Not Available in Inventory"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
                        calc -= int(data["qty"]) * 180
                        dp.quantity = calc
                    elif foodi.drink_metric == "Half":
                        calc = dp.quantity
                        if (int(data["qty"]) * 375) > calc:
                            ordee.delete()
                            return JsonResponse(
                                {"error": foodi.name + " Not Available in Inventory"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
                        calc -= int(data["qty"]) * 375
                        dp.quantity = calc

                    elif foodi.drink_metric == "Full":
                        calc = dp.quantity
                        if (int(data["qty"]) * 750) > calc:
                            ordee.delete()
                            return JsonResponse(
                                {"error": foodi.name + " Not Available in Inventory"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
                        calc -= int(data["qty"]) * 750
                        dp.quantity = calc
                    elif foodi.drink_metric == "Beer Bottle Small":
                        calc = dp.quantity
                        if (int(data["qty"]) * 1) > calc:
                            ordee.delete()
                            return JsonResponse(
                                {"error": foodi.name + " Not Available in Inventory"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
                        calc -= int(data["qty"]) * 1
                        dp.quantity = calc
                    else:
                        if foodi.drink_metric == "Glass":
                            if foodi.type_of_drink == "Beer":
                                calc = dp.quantity
                                if (float(data["qty"]) * 0.5) > calc:
                                    ordee.delete()
                                    return JsonResponse(
                                        {
                                            "error": foodi.name
                                            + " Not Available in Inventory"
                                        },
                                        status=status.HTTP_403_FORBIDDEN,
                                    )
                                calc -= float(float(data["qty"]) * 0.5)
                                dp.quantity = calc
                            elif foodi.type_of_drink == "Wine":
                                calc = dp.quantity
                                if (int(data["qty"]) * 150) > calc:
                                    ordee.delete()
                                    return JsonResponse(
                                        {
                                            "error": foodi.name
                                            + " Not Available in Inventory"
                                        },
                                        status=status.HTTP_403_FORBIDDEN,
                                    )
                                calc -= float(int(data["qty"]) * 150)
                                dp.quantity = calc
                            else:
                                calc = dp.quantity
                                if (int(data["qty"]) * 250) > calc:
                                    ordee.delete()
                                    return JsonResponse(
                                        {
                                            "error": foodi.name
                                            + " Not Available in Inventory"
                                        },
                                        status=status.HTTP_403_FORBIDDEN,
                                    )
                                calc -= float(int(data["qty"]) * 250)
                                dp.quantity = calc

                        else:
                            if foodi.type_of_drink == "Wine":
                                calc = dp.quantity
                                if (int(data["qty"]) * 1000) > calc:
                                    ordee.delete()
                                    return JsonResponse(
                                        {
                                            "error": foodi.name
                                            + " Not Available in Inventory"
                                        },
                                        status=status.HTTP_403_FORBIDDEN,
                                    )
                                calc -= float(int(data["qty"]) * 1000)
                                dp.quantity = calc
                            else:
                                calc = dp.quantity
                                if (int(data["qty"]) * 1) > calc:
                                    ordee.delete()
                                    return JsonResponse(
                                        {
                                            "error": foodi.name
                                            + " Not Available in Inventory"
                                        },
                                        status=status.HTTP_403_FORBIDDEN,
                                    )
                                calc -= float(int(data["qty"]) * 1)
                                dp.quantity = calc

                    dp.save()
                except:
                    pass

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


""" @api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def paymentt(request):
    try:
        datas = JSONParser().parse(request)
        idd = request.user.id
        discount_typee = "Percentage"
        discount_valuee = 0.0
        discount_percentagee = 0
        amountt = 0
        if datas["discount_type"]:
            discount_typee = datas["discount_type"]

        if datas["discount_value"]:
            discount_valuee = datas["discount_value"]

        if datas["discount_percentage"]:
            discount_percentagee = datas["discount_percentage"]

        if datas["amount_paid"]:
            amountt = datas["amount_paid"]

        userr = User.objects.get(id=idd)
        tablee = Table.objects.get(table_name=datas["table_name"])
        paymentmethod = PaymentMethod.objects.get(
            payment_method_name=datas["payment_method"]
        )
        ordee = Order.objects.filter(table=tablee)

        for ord in ordee:
            ord.status = "Order Paid"
            ord.save()

        payme = Payment.objects.create(
            user=userr,
            payment_method=paymentmethod,
            status="Paid",
            table=tablee,
            discount_type=discount_typee,
            discount=discount_valuee,
            discount_percentage=discount_percentagee,
            amount_paidd=amountt,
        )
        payme.order.set(ordee)

        if paymentmethod.payment_method_name == "Card":
            payme.bank_name = datas["bank_name"]

        if datas["payment_remarks"]:
            payme.payment_remarks = datas["payment_remarks"]

        payme.save()

        return JsonResponse(
            {"success": "Payment Submission Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Order Payment Failed"}, status=status.HTTP_400_BAD_REQUEST
        )
 """


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def paymentt(request):
    try:
        datas = JSONParser().parse(request)
        idd = request.user.id
        userr = User.objects.get(id=idd)
        tablee = Table.objects.get(table_name=datas["table_name"])
        paymentmethod = PaymentMethod.objects.get(
            payment_method_name=datas["payment_method"]
        )
        ordee = Order.objects.filter(table=tablee, status="Order Completed")
        for ord in ordee:
            ord.status = "Order Paid"
            ord.save()
            for itemm in ord.orderitems.all():
                itemm.status = "Order Paid"
                itemm.save()

        payme = Payment.objects.create(
            user=userr,
            payment_method=paymentmethod,
            status="Paid",
            table=tablee,
            tender_amount=datas["tender_amount"],
            customer_name=datas["customer_name"],
            pan_no=datas["pan_no"],
            discount_type=datas["discount_type"],
            discount=datas["discount_value"],
            discount_percentage=datas["discount_percentage"],
            amount_paidd=datas["amount_paid"],
        )
        payme.order.set(ordee)

        if paymentmethod.payment_method_name == "Card":
            payme.bank_name = datas["bank_name"]
        """ try:
            if datas["payment_remark"]:
                payme.payment_remarks = datas["payment_remark"]
        except:
            pass """
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
