#! /usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import json
from flask import Flask, request, send_file, redirect
from StringIO import StringIO
from wxpay import QRWXpay, JSWXpay


app = Flask(__name__)
qr_wxpay = QRWXpay(appid='your appid',
                   mch_id='your mch_id',
                   key='your key',
                   ip='your server ip',
                   notify_url='your noifty url',
                   appsecret='your appsecret')
js_wxpay = JSWXpay(appid='your appid',
                   mch_id='your mch_id',
                   key='your key',
                   ip='your server ip',
                   notify_url='your noifty url',
                   appsecret='your appsecret')


@app.route('/paytest/')
def main():
    ret_str = '''
    <a href="/paytest/qr_1">mode 1</a>
    <a href="/paytest/qr_2">mode 2</a>
    <a href="/paytest/jsapi">jsapi</a>
    '''
    return ret_str


@app.route('/paytest/qr_1')
def qr_1():
    product_id = '12345'
    img = qr_wxpay.generate_static_qr(product_id)
    img_io = StringIO()
    img.save(img_io)  # 直接将生成的QR放在了内存里, 请根据实际需求选择放在内存还是放在硬盘上
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/paytest/qr_1/callback', methods=['GET', 'POST'])
def get_product():
    xml_str = request.data
    ret, ret_dict = qr_wxpay.verify_callback(xml_str)
    if ret:
        # 根据实际情况生成product
        product = {
            'attach': u'标题',
            'body': u'内容',
            'out_trade_no': 11111,
            'total_fee': 0.01,
        }
        uni_dict = qr_wxpay.unifiedorder(product)
        resp_dict = {
            'prepay_id': uni_dict['prepay_id'],
            'return_code': 'SUCCESS',  # 'SUCCESS', 'FAIL'
            'return_msg': 'OK',  # 'OK'
            'result_code': 'SUCCESS',  # 'SUCCESS', 'FAIL'
            'err_code_des': 'OK',  # 'OK'
        }
        ret_xml = qr_wxpay.generate_cb_resp(resp_dict)
    else:
        # 检查下单失败的情况
        resp_dict = {
            'prepay_id': 0,
            'return_code': 'FAIL',  # 'SUCCESS', 'FAIL'
            'return_msg': 'unifiedorder error',  # 'OK'
            'result_code': 'FAIL',  # 'SUCCESS', 'FAIL'
            'err_code_des': 'unifiedorder error',  # 'OK'
        }
        ret_xml = qr_wxpay.generate_cb_resp(resp_dict)
    return ret_xml


@app.route('/paytest/qr_2')
def qr_2():
    product = {
        'attach': u'标题',
        'body': u'内容',
        'out_trade_no': 22222,
        'total_fee': 0.01,
    }
    img = qr_wxpay.generate_product_qr(product)
    img_io = StringIO()
    img.save(img_io)  # 直接将生成的QR放在了内存里, 请根据实际需求选择放在内存还是放在硬盘上
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/paytest/jsapi')
def jsapi():
    info_dict = {
        'redirect_uri': 'http://wxapi.getvinci.com/paytest/jsapi/makepayment',
        'state': '123',
    }
    url = js_wxpay.generate_redirect_url(info_dict)
    return redirect(url)


@app.route('/paytest/jsapi/makepayment')
def jsapi_makepayment():
    print request.args
    code = request.args.get('code')
    state = request.args.get('state')
    openid = js_wxpay.generate_openid(code)
    product = {
        'attach': u'标题',
        'body': u'内容',
        'out_trade_no': 33333,
        'total_fee': 0.01,
    }
    ret_dict = js_wxpay.generate_jsapi(product, openid)
    ret_str = '''
    <html>
    <head></head>
    <body>
    <script type="text/javascript">
    function callpay()
    {
        if (typeof WeixinJSBridge == "undefined"){
            if( document.addEventListener ){
                document.addEventListener('WeixinJSBridgeReady', jsApiCall, false);
            }else if (document.attachEvent){
                document.attachEvent('WeixinJSBridgeReady', jsApiCall); 
                document.attachEvent('onWeixinJSBridgeReady', jsApiCall);
            }
        }else{
            jsApiCall();
        }
    }
    alert("ddd");
    function jsApiCall(){
        alert("in");
        WeixinJSBridge.invoke(
            'getBrandWCPayRequest',
            %s,
            function(res){
                alert(JSON.stringify(res));
            }
        );
    }
    callpay();
    </script>
    </body>
    </html>
    ''' % json.dumps(ret_dict)

    return ret_str


@app.route('/paytest/notify', methods=['GET', 'POST'])
def notify():
    xml_str = request.data
    ret, ret_dict = qr_wxpay.verify_notify(xml_str)
    # 在这里添加订单更新逻辑
    if ret:
        ret_dict = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK',
        }
        ret_xml = qr_wxpay.generate_notify_resp(ret_dict)
    else:
        ret_dict = {
            'return_code': 'FAIL',
            'return_msg': 'verify error',
        }
        ret_xml = qr_wxpay.generate_notify_resp(ret_dict)
    return ret_xml

@app.route('/paytest/order/<order_id>', methods=['GET'])
def order(order_id):
    xml_dict = qr_wxpay.verify_order(out_trade_no=order_id)
    return json.dumps(xml_dict)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
