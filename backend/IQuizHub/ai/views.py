import base64
import os
import uuid

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from utils.ocr_bot import ocr
from utils.yichat import ask


# Create your views here.

class AiViewSet(viewsets.ModelViewSet):


    def ask(self, request, *args, **kwargs):
        content = request.data.get('content')
        if not content:
            return Response({'error': '缺少content参数'}, status=400)

        res = ask(content)
        return Response({'result': res['result']}, status=200)

    def ocr_pic(self, request):
        base64_img = request.data.get('base64_img')
        if not base64_img:
            return Response({'error': 'base64_img is required'}, status=400)
        try:
            result = ocr(base64_img)
        except:
            return Response({'error': 'OCR failed'}, status=400)

        txts = result[1]
        image = result[0]
        relative_path = os.path.join('files', 'ocr_res')
        if not os.path.exists(relative_path):
            os.makedirs(relative_path)
        image_filename = uuid.uuid4().hex + '.jpg'
        image_path = os.path.join(relative_path, image_filename)
        image.save(image_path)

        image_url = request.build_absolute_uri('/' + image_path.replace('\\', '/'))

        return Response({
            'image_url': image_url,
            'texts': txts
        })
