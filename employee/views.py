from urllib import response
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import services


@api_view(['POST'])
def onboard(request):
    print(request.META['HTTP_AUTHORIZATION'])
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.onboard(token, request.data)
    except KeyError as e:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'NO TOKEN FOUND'
        }
    return Response(response, status=response['code'])


@api_view(['GET'])
def get_all_employee(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        q = request.GET.get("q")
        if q == 'all':
            response = services.get_employee(token, isAll=True)
        elif q != '' and q.isnumeric():
            response = services.get_employee(token, isAll=True, id=q)
        else:
            response = {
                'status': False,
                'message': 'Invalid Parameter',
                'code': status.HTTP_400_BAD_REQUEST
            }
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid token, Key Error',
            'code': status.HTTP_406_NOT_ACCEPTABLE
        }
    return Response(response, status=response['code'])


@api_view(['PUT'])
def update_employee(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        body = request.data
        response = services.update_employee(token, body)
    except KeyError:
        response = {
            'status': False,
            'message': 'Invalid token, Key Error',
            'code': status.HTTP_406_NOT_ACCEPTABLE
        }
    return Response(response, status=response['code'])


@api_view(['GET'])
def get_manager(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        q = request.GET.get("q")
        if q == 'all':
            response = services.get_manager(token, isAll=True)
        elif q != '' and q.isnumeric():
            response = services.get_employee(token, isAll=True, id=q)
        else:
            response = {
                'status': False,
                'message': 'Invalid Parameter',
                'code': status.HTTP_400_BAD_REQUEST
            }
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid token, Key Error',
            'code': status.HTTP_406_NOT_ACCEPTABLE
        }
    return Response(response, status=response['code'])


@api_view(['GET'])
def get_department(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        q = request.GET.get("q")
        if q == 'all':
            response = services.get_department(token, isAll=True)
        elif q != '' and q.isnumeric():
            response = services.get_department(token, isAll=True, id=q)
        else:
            response = {
                'status': False,
                'message': 'Invalid Parameter',
                'code': status.HTTP_400_BAD_REQUEST
            }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Key Error'
        }
    return Response(response, status=response['code'])


@api_view(['GET'])
def get_hardware(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        q = request.GET.get("q")
        if q == 'my':
            response = services.get_hardware(token)
        elif q != '' and q.isnumeric():
            response = services.get_hardware(token, id=q)
        else:
            response = {
                'status': False,
                'message': 'Invalid Parameter',
                'code': status.HTTP_400_BAD_REQUEST
            }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Key Error'
        }
    return Response(response, status=response['code'])

@api_view(['POST'])
def make_manager(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.make_manager(token, request.data)
    except Exception as e:
        response = {
            'status':False,
            'code':status.HTTP_400_BAD_REQUEST,
            'message':str(e)
        }
    return Response(response, status=response['code'])


@api_view(['GET'])
def leave_counts(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.leave_counts(token)
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid token, Key Error',
            'code': status.HTTP_406_NOT_ACCEPTABLE
        }
    return Response(response, status=response['code'])
