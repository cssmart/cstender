import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import api_view
import ast


@api_view(['POST'])
def whatsapp(request):
    data = request.data

    TEMPLATE_NAME = data['TEMPLATE_NAME']
    TO_NUMBER = data['TO_NUMBER']
    parameterValues = data['parameterValues']
    parameterValues = ast.literal_eval(parameterValues)
    print(parameterValues,"para=======================")

    while ("null" in parameterValues):
        parameterValues.remove("null")
    parameter_values = {i: parameterValues[i] for i in range(0, len(parameterValues))}

    headers = {'Content-Type': 'application/json',
                   'Authentication': 'Bearer gbGdau3EbVNJCCxd0BxNfg=='}
    json = {
        "message":{
                    "channel":"WABA",
                    "content":{
                        "preview_url":'false',
                        "shorten_url":'false',
                        "type":"TEMPLATE",
                        "template":{
                            "templateId":TEMPLATE_NAME,
                            "parameterValues": parameter_values
                             }
                 },
                "recipient":{
                    "to":TO_NUMBER,
                    "recipient_type":"individual",
                    "reference":{
                        "cust_ref":"cust_ref123",
                        "messageTag1":"Message Tag 001",
                        "conversationId":"Conv_123"
                            }
                },
                "sender":{
                    "name":"Whatsappdemo",
                    "from":"919999567202"
                  },
                "preferences":{
                    "webHookDNId":"1001"
                }
         },
                "metaData":{
                    "version":"v1.0.9"
                }
         }
    try:
        response = requests.post("https://rcmapi.instaalerts.zone/services/rcm/sendMessage", timeout=5, json=json,
                                 headers=headers)
    except:
        try:
            response = requests.post("https://rcmapi.instaalerts.zone/services/rcm/sendMessage", timeout=5, json=json,
                                     headers=headers)
            return Response(response)
        except:
            return Response("Session Time Out")
    return HttpResponse(response)
