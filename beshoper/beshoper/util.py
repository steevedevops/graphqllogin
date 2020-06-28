from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Page as PaginatorPage
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.conf import settings

from geralapi.models import *
from proprietarioapi.models import *

from os import walk

import json
import requests
from random import randint
from datetime import datetime

class Util:

    def getObjectFromJson(payload, model, appname, dataType = 'json'):
        payload['model'] = '%s.%s' % (appname, model)
        if not isinstance(payload, list):
            for i in serializers.json.Deserializer(json.dumps([payload])):
                return i
        else:
            objects = []
            for i in serializers.json.Deserializer(json.dumps(payload)):
                objects.append(i)

            return objects
        return None

    def getPayload(request):
        return json.loads(request.body.decode()) if request.body.decode() != '' else {}

    def setResponse(data):
        return HttpResponse(JsonResponse(data, safe=False).content, content_type="application/json")

    def setErrorResponse(data, code=500):
        return HttpResponse(JsonResponse(data, safe=False).content, content_type="application/json", status=code)

    def serializeResponse(data):
        data, single = [[data], True] if type(data) != list and type(data) != PaginatorPage and type(data) != QuerySet else [data, False]

        results = json.loads(serializers.serialize('json', data))
        for result in results:
            if result.__contains__('model'):
                if result.__contains__('fields') and result['fields'].__contains__('password'):
                    result['fields'].pop('password')

        if single:
            return results[0]
        else:
            return results

    def getFullDomain(request):
        return ('%s://%s' % (request.get_raw_uri().split('://')[0], request.get_host()))

    def recaptcha(secret, token):
        '''
        Score less then 3 then it's a boot.
        Scoring greater then 3.1 it's human
        '''
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data={"secret":secret, "response":token}).json()
        print ('Answer from google recaptcha: ', resp)
        if resp['success']:
            return resp['score']
        else:
            print ('Recaptcha Error: ', str(resp['error-codes']))
        return 0

    def generateCode(characters='123456789abcdefghijklmnopqrstuvxyzABCDEFGHIJKMLNOPQRSTUVXYZ', size=6):
        return User.objects.make_random_password(length=size, allowed_chars=characters)

    def getCidadeByCEPViaCep(cep):
        resp = requests.get('https://viacep.com.br/ws/%s/json/' % cep).json()
        return resp

    def getCidadeByCEPCepaberto(cep):
        token = "d657c8a94032cf3dabd7232b36277c96"
        resp = requests.get('http://www.cepaberto.com/api/v3/cep?cep=%s' % cep, headers={'Authorization': 'Token token=%s' % token}).json()
        return resp

class BooleanFieldParse():

    TRUE_VALUES = {
        't', 'T',
        'y', 'Y', 'yes', 'YES',
        'true', 'True', 'TRUE',
        'on', 'On', 'ON',
        '1', 1,
        True
    }
    FALSE_VALUES = {
        'f', 'F',
        'n', 'N', 'no', 'NO',
        'false', 'False', 'FALSE',
        'off', 'Off', 'OFF',
        '0', 0, 0.0,
        False
    }

    def __init__(self, data):
        self.data = data

    def parse(self):
        if self.data in self.TRUE_VALUES:
            return True
        elif self.data in self.FALSE_VALUES:
            return False

        return None
