from django.shortcuts import render, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .models import Bank, PaymentMethod
from .serializers import BankSerializer, PaymentMethodSerializer
from rest_framework.response import Response


@api_view(["GET"])
def banklists(request):
    banks = Bank.objects.all()
    banks_serializer = BankSerializer(banks, many=True)
    return Response(banks_serializer.data)


@api_view(["GET"])
def paymentmethodlists(request):
    payment = PaymentMethod.objects.all()
    payments_serializer = PaymentMethodSerializer(payment, many=True)
    return Response(payments_serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addBank(request):
    try:
        datas = JSONParser().parse(request)
        bank = Bank.objects.create(bank_name=datas["bank_name"])
        bank.save()

        return JsonResponse(
            {"success": "Bank Created Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Bank Addition Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singleBank(request, id):
    try:
        bank = Bank.objects.get(id=id)
        bank_serializer = BankSerializer(bank)
        return Response(bank_serializer.data)
    except:
        return JsonResponse(
            {"error": "Invalid Bank"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBank(request):
    try:
        datas = JSONParser().parse(request)
        bank = Bank.objects.get(id=datas["id"])
        bank.bank_name = datas["bank_name"]
        bank.save()
        return JsonResponse(
            {"success": "Bank Updated Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Bank Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteBank(request):
    try:
        datas = JSONParser().parse(request)
        bank = Bank.objects.get(id=datas["id"])
        bank.delete()

        return JsonResponse(
            {"success": "Bank Delete Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Bank Delete Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addPaymentMethod(request):
    try:
        datas = JSONParser().parse(request)
        payment = PaymentMethod.objects.create(
            payment_method_name=datas["payment_method_name"]
        )
        payment.save()

        return JsonResponse(
            {"success": "Payment Method Created Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Payment Method Addition Failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singlePaymentMethod(request, id):
    try:
        payment = PaymentMethod.objects.get(id=id)
        payment_serializer = PaymentMethodSerializer(payment)
        return Response(payment_serializer.data)
    except:
        return JsonResponse(
            {"error": "Invalid Payment Method"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updatePaymentMethod(request):
    try:
        datas = JSONParser().parse(request)
        payment = PaymentMethod.objects.get(id=datas["id"])
        payment.payment_method_name = datas["payment_method_name"]
        payment.save()
        return JsonResponse(
            {"success": "Payment Method Updated Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Payment Method Update Failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deletePaymentMethod(request):
    try:
        datas = JSONParser().parse(request)
        payment = PaymentMethod.objects.get(id=datas["id"])
        payment.delete()

        return JsonResponse(
            {"success": "Payment Method Delete Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Payment Method Delete Failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
