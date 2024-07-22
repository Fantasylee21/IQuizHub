from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from utils.yichat import ask


# Create your views here.

class AiViewSet(viewsets.ModelViewSet):

    def ask(self, request, *args, **kwargs):
        content = request.data.get('content')
        if not content:
            return Response({'error': '缺少content参数'}, status=400)

        res = ask(content)
        return Response({'result': res['result']}, status=200)
