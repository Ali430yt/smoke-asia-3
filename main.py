from flask import Flask,request,render_template,jsonify ,session
from flask_cors import CORS
from datetime import datetime, timedelta
import requests,time,json
from uuid import uuid4
from telebot import TeleBot


key = "KBAUKtMjbGmszaiU30Rx55U5UfnJqlodRUADojOvdAYBDcPAlLPvlFBD2iyZ"
PicX = 1000

def CilentUser(login,amount=0):
    api = f"https://socpanel.com/privateApi/incrementUserBalance?login={login}&amount={amount}&token={key}"
    r = requests.get(api)
    if not "error" in r.json():
        return True
    else:
        return False


app = Flask(__name__)
app.secret_key = "wr923-*389110lalwke-brbdjzoakwm-wjeirofojcn-akwmebdk-sokiopasdfg-hjlzmsmak-ao991203k-aksbek"
app.config['PERMANENT_SESSION_LIFETIME'] = 30 * 24 * 60 * 60  # 30 days
CORS(app)



def sendTele(username,kmi,cart=None):
    tk = "7843250449:AAF5wHxmLl4SWjbK5QBcqFPIkrK_Cmf1WP0"
    ids = ["1044160205","7394840718"]
    tp = str(time.strftime('%Y-%m-%d-%H:%M:%S'))
    if cart == None:
        text = f"عملية شحن جديد ✅\nأسم المستخدم : {username} 👤\nالمبلغ المشحون : {str(kmi)}$ 💰\nالتاريخ : {tp}"
    else:
        text = f"عملية شحن جديد ✅\nأسم المستخدم : {username} 👤\nالمبلغ المشحون : {str(kmi)}$ 💰\nالتاريخ : {tp} \nنوع العملية : كارت 💳 \nرقم الكارت : {cart}"
    #bot = TeleBot(tk)
    #for id in ids:
        #try:bot.send_message(chat_id=id,text=text)
        #except:pass
        


def getme(session):
    if "login" in session and session["login"] == True:
        url = "https://odpapp.asiacell.com/api/v2/home?lat=0.0&lng=0.0&roaming=false&lang=en"
        headers = {
        'User-Agent': "okhttp/5.0.0-alpha.2",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'X-ODP-API-KEY': "1ccbc4c913bc4ce785a0a2de444aa0d6",
        'DeviceID': session["sid-login"],
        'X-OS-Version': "14",
        'X-Device-Type': "[Android][TECNO][TECNO LI9 14][TIRAMISU][GMS][4.0.9:90000217]",
        'X-ODP-APP-VERSION': "4.3.6",
        'X-FROM-APP': "odp",
        'X-ODP-CHANNEL': "mobile",
        'X-SCREEN-TYPE': "MOBILE",
        'Authorization': f"Bearer {session["access_token"]}",
        'Cache-Control': "private, max-age=240",
        'If-Modified-Since': "Thu, 08 May 2025 00:53:33 GMT",
        }
        try:
            response = requests.get(url, headers=headers)
            if "Prepaid balance" in response.text:
                analyticData = response.json()["analyticData"]["props"]
                coin = int(analyticData["Prepaid balance"])
                return coin
            else: 
                return 0
        except:
            return 0
    return 0
@app.route("/")
def index():
    session.permanent = True
    if "login" in session and session["login"] == True:
        url = "https://odpapp.asiacell.com/api/v2/home?lat=0.0&lng=0.0&roaming=false&lang=en"
        headers = {
        'User-Agent': "okhttp/5.0.0-alpha.2",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'X-ODP-API-KEY': "1ccbc4c913bc4ce785a0a2de444aa0d6",
        'DeviceID': session["sid-login"],
        'X-OS-Version': "14",
        'X-Device-Type': "[Android][TECNO][TECNO LI9 14][TIRAMISU][GMS][4.0.9:90000217]",
        'X-ODP-APP-VERSION': "4.3.6",
        'X-FROM-APP': "odp",
        'X-ODP-CHANNEL': "mobile",
        'X-SCREEN-TYPE': "MOBILE",
        'Authorization': f"Bearer {session["access_token"]}",
        'Cache-Control': "private, max-age=240",
        'If-Modified-Since': "Thu, 08 May 2025 00:53:33 GMT",
        }
        response = requests.get(url, headers=headers)
        if "Prepaid balance" in response.text:
            analyticData = response.json()["analyticData"]["props"]
            try:
                name = analyticData["Name"]
            except:
                name = "يرجى تسجيل الخروج"
            try:
                coin = analyticData["Prepaid balance"]
            except:
                coin = "لايوجد"
            try:
                phone = session["phone-login"]
            except:
                phone = ""
            
            data = {"islogin":True,"name":name,"phone":phone,"coin":coin}
            #return {"ok":True,"coin":analyticData["Prepaid balance"],"number":mydata[1]}
        else: 
            data = {"islogin":False}
        
    else:
        data = {"islogin":False}
    return render_template("asia.html",data=data)

@app.route("/api/login",methods=["POST"])
def ApiLogin():
    session.permanent = True
    data = request.get_json()
    phone = data.get('phone')
    if not phone:
        return jsonify({'ok':'error','text': 'رقم الهاتف مطلوب'}), 400
    phone = str(phone).replace(" ","").strip()
    if not len(str(phone)) == 11:
        return jsonify({'ok':'error','text': 'يجب ان يكون طول رقم 11 رقم فقط'}), 400
    if not str(phone)[:3] == "077":
        return jsonify({'ok':'error','text': 'يجب أرسال رقم اسياسيل فقط'}), 400
    sid = str(uuid4())
    url = "https://odpapp.asiacell.com/api/v1/login?lang=ar"
    headers ={
    "DeviceID": sid,
    'User-Agent': "okhttp/5.0.0-alpha.2",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/json",
    'X-ODP-API-KEY': "1ccbc4c913bc4ce785a0a2de444aa0d6",
    'Cache-Control': "no-cache",
    'X-OS-Version': "14",
    'X-Device-Type': "[Android][TECNO][TECNO LI9 14][TIRAMISU][HMS][4.2.0:90000256]",
    'X-ODP-APP-VERSION': "4.3.6",
    'X-FROM-APP': "odp",
    'X-ODP-CHANNEL': "mobile",
    'X-SCREEN-TYPE': "false",
    'Content-Type': "application/json; charset=UTF-8",
    }
    data = {"captchaCode":"","username":str(phone)}
    r = requests.post(url,headers=headers,data=json.dumps(data)).json()
    if r["success"]:
        pid = str(r["nextUrl"]).split("PID=")[1]
        session["pid-login"] = pid
        session["sid-login"] = sid
        session["phone-login"] = phone
        return jsonify({
            'ok':'ok'
            }), 200
    else:
        text = "فشل أرسال كود التحقق رمز الخطأ :"
        return jsonify({
            'ok':'error',
            'text':text
            }), 400


@app.route("/api/smsvalidation",methods=["POST"])
def ApiSmsvalidation():
    session.permanent = True
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'ok':'error','text': 'الكود مطلوب'}), 400
    if not len(str(code).strip()) == 6:
        return jsonify({'ok':'error','text': 'يجب ان يكون طول الكود من 6 ارقام'}), 400
    if "pid-login" in session and "sid-login" in session and "phone-login" in session:
        pass
    else:
        return jsonify({'ok':'error','text': 'حدثت مشكلة في طلبك'}), 400
    sid = session["sid-login"]
    pid = session["pid-login"]
    url = "https://odpapp.asiacell.com/api/v1/smsvalidation?lang=ar"
    headers ={
    "X-ODP-API-KEY": "1ccbc4c913bc4ce785a0a2de444aa0d6",
    "DeviceID": sid,
    "X-OS-Version": "11",
    "X-Device-Type": "[Android][realme][RMX2001 11] [Q]",
    "X-ODP-APP-VERSION": "4.3.6",
    "X-FROM-APP": "odp",
    "X-ODP-CHANNEL": "mobile",
    "X-SCREEN-TYPE": "MOBILE",
    "Cache-Control": "private, max-age=240",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "43",
    "Host": "odpapp.asiacell.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/5.0.0-alpha.2"}

    data = {"PID":str(pid),"passcode":str(code),"token":"e1OrgWG9T4mzVKZS4N9EqT:APA91bFxGBHePpzolWWPtl4ICO6UV5y5W7HrPa-kKNz2mEBCuD-a3en50n-EE4dpMwEEfxUt4Lr-ai_hAatoGDDcwNbBKaQ-3Mn3CkMmO1MlXjKZoQuR06NlvdqYJ53uUC2SODMKpznD"}
    r = requests.post(url,headers=headers,json=data).json()
    if r["success"]:
        session["access_token"] = str(r["access_token"])
        session["login"] = True
        return jsonify({
            'ok':'ok'
            }), 200 
    else:
        text = "كود تحقق خطأ"
        return jsonify({
            'ok':'error',
            'text':text
            }), 400


@app.route("/api/cart",methods=["POST"])
def ApiCart():
    session.permanent = True
    if "login" in session and session["login"] == True:
        data = request.get_json()
        code = data.get('code')
        username = data.get('username')
        if not code:
            return jsonify({'ok':'error','text': 'الكود مطلوب'}), 400
        if not username:
            return jsonify({'ok':'error','text': 'اسم المستخدم مطلوب'}), 400
        sid = session["sid-login"]
        pid = session["pid-login"]
        access_token = session["access_token"]
        target = "07727165554"
        if CilentUser(username):
            url = "https://odpapp.asiacell.com/api/v1/top-up?lang=ar"
            payload = {
            "msisdn": target,
            "rechargeType": 1,
            "voucher": code
            }
            headers = {
  'User-Agent': "okhttp/5.1.0",
  'Connection': "Keep-Alive",
  'Accept-Encoding': "gzip",
  'Content-Type': "application/json",
  'X-ODP-API-KEY': "1ccbc4c913bc4ce785a0a2de444aa0d6",
  'Cache-Control': "no-cache",
  'DeviceID':sid,
  'X-OS-Version': "15",
  'X-Device-Type': "[Android][TECNO][TECNO LI9 15][VANILLA_ICE_CREAM][GMS][4.3.7:90000323]",
  'X-ODP-APP-VERSION': "4.3.7",
  'X-FROM-APP': "odp",
  'X-ODP-CHANNEL': "mobile",
  'X-SCREEN-TYPE': "MOBILE",
  'Authorization': f"Bearer {access_token}",
  'Content-Type': "application/json; charset=UTF-8"
            }
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            js = response.json()
            print(js)
            if js["success"]:
                kmi = int(float(js["analyticData"]["params"]["Recaharge amount"]) / 1000)
                text = f"تم شحن حساب ب {kmi}$ ✅"
                CilentUser(login=username,amount=kmi)
                sendTele(username,str(kmi),cart=str(code))
                return jsonify({'ok':'ok','text': text}), 200
            else:
                text = js["message"]
                return jsonify({'ok':'error','text': text,'js':js}), 400
        else:
            return jsonify({'ok':'error','text': 'أسم المستخدم غير موجود'}), 400
    else:
        return jsonify({'ok':'error','text': 'يرجى تسجيل الدخول'}), 400


@app.route("/api/getpidpay",methods=["POST"])
def ApiGetPidPay():
    session.permanent = True
    if "login" in session and session["login"] == True:
        data = request.get_json()
        coin = data.get('coin')
        username = data.get('username')
        if not coin:
            return jsonify({'ok':'error','text': 'الكمية مطلوبة'}), 400
        if not username:
            return jsonify({'ok':'error','text': 'اسم المستخدم مطلوب'}), 400
        coin = int(coin)
        sid = session["sid-login"]
        pid = session["pid-login"]
        access_token = session["access_token"]
        target = "07727165554"
        if CilentUser(username):
            url = "https://odpapp.asiacell.com/api/v1/credit-transfer/start?lang=ar"
            headers ={
            "X-ODP-API-KEY": "1ccbc4c913bc4ce785a0a2de444aa0d6",
            "DeviceID": sid,
            "Authorization": f"Bearer {access_token}",
            "X-OS-Version": "11",
            "X-Device-Type": "[Android][realme][RMX2001 11] [Q]",
            "X-ODP-APP-VERSION": "4.3.6",
            "X-FROM-APP": "odp",
            "X-ODP-CHANNEL": "mobile",
            "X-SCREEN-TYPE": "MOBILE",
            "Cache-Control": "private, max-age=240",
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "43",
            "Host": "odpapp.asiacell.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/5.0.0-alpha.2"}
            data = {"amount":f"{coin}","receiverMsisdn":str(target)}
            req = requests.post(url,headers=headers,json=data)
            r = req.json()
            print(r)
            if not "success" in r:
                return jsonify({'ok':'error','text': 'يرجى تسجيل الخروج ودخول مرة ثانية لتحقق من الجلسة'}), 400
            if r["success"]:
                pidTransfer = str(r["PID"])
                session["kmi"] = float(float(coin) / PicX)
                session["pidTransfer"] = pidTransfer
                session["username"] = str(username)
                return jsonify({'ok':'ok'}), 200
            else:
                return jsonify({'ok':'error','text': 'لايوجد رصيد كافي في حسابك ملاحضة عمولة تحويل هي 350 دينار'}), 400
        else:
            return jsonify({'ok':'error','text': 'أسم المستخدم غير موجود'}), 400
    else:
        return jsonify({'ok':'error','text': 'يرجى تسجيل الدخول'}), 400





@app.route("/api/do-transfer",methods=["POST"])
def DoTransfer():
    session.permanent = True
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'ok':'error','text': 'الكود مطلوب'}), 400
    if not len(str(code).strip()) == 6:
        return jsonify({'ok':'error','text': 'يجب ان يكون طول الكود من 6 ارقام'}), 400
    if "kmi" in session and "pidTransfer" in session:
        pass
    else:
        return jsonify({'ok':'error','text': 'حدثت مشكلة في طلبك'}), 400
    kmi = session["kmi"]
    pidTransfer = session["pidTransfer"]
    sid = session["sid-login"]
    access_token = session["access_token"]
    username = session["username"]
    url = "https://odpapp.asiacell.com/api/v1/credit-transfer/do-transfer?lang=en"
    headers = {
    "X-ODP-API-KEY": "1ccbc4c913bc4ce785a0a2de444aa0d6",
    "DeviceID": sid,
    "Authorization": f"Bearer {access_token}",
    "X-OS-Version": "11",
    "X-Device-Type": "[Android][realme][RMX2001 11] [Q]",
    "X-ODP-APP-VERSION": "4.3.7",
    "X-FROM-APP": "odp",
    "X-ODP-CHANNEL": "mobile",
    "X-SCREEN-TYPE": "MOBILE",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "43",
    "Host": "odpapp.asiacell.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/5.0.0-alpha.2"}

    data = {"PID":pidTransfer,"passcode":str(code)}
    r = requests.post(url,headers=headers,json=data).json()
    if r["success"]:
        req = CilentUser(username,str(kmi))
        sendTele(username,kmi)
        text = f"تم شحن حسابك بقيمة : {kmi} ✅"
        return jsonify({
            'ok':'ok',
            'text':text
            }), 200 
    else:
        text = "كود تحقق خطأ او خطأ بل أتصال"
        return jsonify({
            'ok':'error',
            'text':text,
            'js':r
            }), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)











