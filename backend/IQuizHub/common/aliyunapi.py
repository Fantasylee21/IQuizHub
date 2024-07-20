# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import json
import os
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions


class AliyunSMS:
    access_key_id = 'LTAI5tHxPtFrnGb2gCwr8N3K'
    access_key_secret = 'nc9uv9z4SvDyrXVW8xTCrBzYVm6Po8'
    endpoint = 'dysmsapi.aliyuncs.com'
    sign_name = '阿里云短信测试'
    template_code = 'SMS_154950909'

    def __init__(self):
        self.config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint=f'dysmsapi.aliyuncs.com',
        )

    def send_sms(self, mobile: str, code: str):
        client = Client(self.config)
        send_sms_request = SendSmsRequest(
            phone_numbers=mobile,
            template_param=json.dumps({"code": code}),
            sign_name=self.sign_name,
            template_code=self.template_code,
        )
        runtime = RuntimeOptions()
        try:
            res = client.send_sms_with_options(send_sms_request, runtime)
            if res.body.code == 'OK':
                return {'code': 'ok', 'msg': '发送成功'}
            else:
                return {'code': 'error', 'msg': res.body.message}
        except Exception as e:
            return {'code': 'error', 'msg': str(e)}


if __name__ == '__main__':
    sms = AliyunSMS()
    sms.send_sms('18754558035', '1234')
