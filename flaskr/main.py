from __future__ import print_function
from re import T
import urllib.request
import urllib
import requests
import os.path
import connexion
import json
import datetime
import openpyxl
import pandas as pd
import numpy as np
from os import environ
from ssl import _create_default_https_context
from typing import KeysView
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response
from marshmallow import Schema, fields, pprint
from http import HTTPStatus
from flaskr.Swg import Standard, Status, HomeInfo, ControlRecom, CheckStylerState, Closet, Weather, TodayRecom, AddPrefer, AddClothes, ControlStyler, AddCSV, RecomToday, NeedStyler, Water, ScheduleAlert, Alert, PostAlert
from flaskr.settings import CLEARDB_DATABASE_URL
from werkzeug.exceptions import HTTPException
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from collections import Counter
from marshmallow import Schema, fields
from flasgger import Swagger
from connexion.resolver import RestyResolver
from flasgger import swag_from


app = Flask(__name__)
swagger = Swagger(app)


# Since you’re not creating an event-driven program, turn this feature off.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This causes SQLAlchemy to echo SQL statements it executes to the console.
app.config['SQLALCHEMY_ECHO'] = True

# Database URL received from heroku
app.config['SQLALCHEMY_DATABASE_URI'] = CLEARDB_DATABASE_URL

#  The db variable is what’s imported into the build_database.py
#  program to give it access to SQLAlchemy and the database.
db = SQLAlchemy(app)

# This initializes Marshmallow and allows it to introspect the SQLAlchemy components attached to the app.
ma = Marshmallow(app)



########## DO NOT DELETE THESE IMPORT STATEMENTS ###########


from flaskr.models.user import User, UserSchema
from flaskr.models.clothes import Clothes, clotheSchema
from flaskr.models.scent import Scent
from flaskr.models.clothes_combination import ClothesCombination
from flaskr.models.control import Control, controlSchema
from flaskr.models.recommendation import Recommendation
from flaskr.models.schedule import Schedule
from flaskr.models.styler_alert import StylerAlert, alertSchema
from flaskr.models.user_preference import UserPreference, preferSchema
from flaskr.models.styler import Styler, stylerSchema
from flaskr.models.mirror import Mirror,MirrorSchema


db.create_all()


#############################################################



# 날씨 api 가져오기
def getWeather(city):
    openweather_api_url = "https://api.openweathermap.org/data/2.5/"
    service_key = environ.get('weatherApiKey')

    # API 요청시 필요한 인수값 정의
    ow_api_url = openweather_api_url + "weather"
    payload = "?q=" + str(city) + "&" + "appid=" + service_key + "&lang=kr"
    url_total = ow_api_url + payload

    # API 요청하여 데이터 받기
    req = urllib.request.urlopen(url_total)
    res = req.readline()
    # 받은 값 JSON 형태로 정제하여 반환
    items = json.loads(res)
    return items

## google calendar API
def calendar():
    api_url = "https://www.googleapis.com/calendar/v3/calendars/c_gk3d37vfpjea22cdnv7f92nkdk@group.calendar.google.com/events?orderBy=startTime&singleEvents=true&timeMax="
    service_key = environ.get('googleapi')
    # API 요청시 필요한 인수값 정의
    time_min = (datetime.date.today() + datetime.timedelta(days=-100)).isoformat() + "T00:00:00Z"
    time_max = (datetime.date.today() + datetime.timedelta(days=100)).isoformat() + "T23:59:59Z"
    url_total = api_url + time_max + "&timeMin=" + time_min + "&key=" + service_key
    # API 요청하여 데이터 받기
    req = requests.get(url_total)
    items = req.json()
    return json.dumps(items, ensure_ascii=False)


class weatherSchema(Schema):
    high_temp = fields.Integer()
    low_temp = fields.Integer()
    daily = fields.Integer()


specs_dict = Status().specs_dict
@app.route('/status/<device>', methods=['GET'])
@swag_from(specs_dict)
def status(device):
    new_styler = Styler.query.filter(Styler.id ==1).first()
    new_mirror = Mirror.query.filter(Mirror.id ==1).first()
    schema_st = stylerSchema()
    schema_mi = stylerSchema(only=("id","connection"))
    if device == 'styler':
        result = schema_st.dump(new_styler)
        return jsonify(result)
    elif device == 'mirror':
        result = schema_mi.dump(new_mirror)
        return jsonify(result)
    else:
        return 'device not found'
    
    
    
specs_dict = Standard().specs_dict
@app.route('/users/names/<userid>', methods=['GET'])
@swag_from(specs_dict)
def check_username(userid):
    name = {"username" : User.query.filter_by(id=userid).first().username}
    schema = UserSchema()
    result = schema.dump(name)
    return result


    
## Add user Prefer
specs_dict = AddPrefer().specs_dict
@app.route('/preferences/<userid>',methods = ['POST'])
@swag_from(specs_dict)
def add_prefer(userid):
    json_data = request.get_json()
    schema = preferSchema()
    new_prefer = UserPreference(user_id=userid, scent_id_one = json_data['scentid_one'],scent_id_two = json_data['scentid_two'], scent_id_three = json_data['scentid_three'],fashion_style_one= json_data['fashion_one'], fashion_style_two= json_data['fashion_two'],fashion_style_three= json_data['fashion_three'], color_one=json_data['color_one'], color_two=json_data['color_two'], color_three=json_data['color_three']).create()
    db.session.commit()
    result = schema.dump(new_prefer)
    return result



class HomeSchema(Schema):
    userid = fields.Integer()
    today_date = fields.String()
    today_week = fields.String()
    now_temp = fields.Integer()
    max_temp = fields.Integer()
    min_temp = fields.Integer()
    mirror_connection = fields.Integer()
    styler_connection = fields.Integer()
    styler_water = fields.Integer()
    dehumification_connect = fields.Integer()
    dry_connect = fields.Integer()
    indoor_humidity = fields.Integer()
    indoor_temp = fields.Integer()
    now_mode = fields.String()
    username = fields.String()


## Load Home info
specs_dict = HomeInfo().specs_dict
@app.route('/home/<userid>/<city>',methods = ['GET'])   
@swag_from(specs_dict)
def get_homeinfo(userid,city):
    t = ['월','화','수','목','금','토','일']
    temp = getWeather(city)
    new_styler = Styler.query.filter_by(id=userid).first()
    data = {
    "userid" : userid,
    "username": User.query.filter_by(id=userid).first().username,
    "today_date" : datetime.datetime.today().strftime('%d'),
    "today_week" : t[datetime.datetime.today().weekday()],
    "now_temp" : int(temp['main']['temp'])-273.15,
    "max_temp" : int(temp['main']['temp_max'])-273.15,
    "min_temp" : int(temp['main']['temp_min'])-273.15,
    "mirror_connection" : Mirror.query.filter_by(id=userid).first().connection,
    "styler_connection" : new_styler.connection,
    "styler_water" : new_styler.water_percentage,
    "dehumification_connect" : new_styler.dehumification_connect,
    "dry_connect" : new_styler.dry_connect,
    "indoor_humidity" : new_styler.humidity,
    "indoor_temp" : new_styler.temperature,
    "now_mode" : new_styler.now_mode
    }
    schema = HomeSchema()
    result = schema.dump(data)
    return result
    

specs_dict = Alert().specs_dict
@app.route('/alerts/<userid>',methods = ['GET'])  
@swag_from(specs_dict)
def alert(userid):
    # "오늘의 추천" 알림 (/recommend/today/<city>/<userid> 에 구현)
    # "제어 추천" 알림 (/recommands/control/<userid> 에 구현)
    # "스타일러 상태" 알림(스타일러 가동) (/state/stylers/<userid> 에 구현)
    # "스타일러 상태" 알림(물상태) (/styler/water/<userid>에 구현)
    # "일정" 알림 (/schedule/<userid> 에 구현)

    push = User.query.filter(User.id==userid).first().push
    if push == 0:
        return jsonify("Ms.TROMM의 맞춤형 추천 내역을 보시려면 푸시 알람을 켜주셔야 합니다!")

    values = StylerAlert.query.filter(StylerAlert.user_id==userid).all()
    dict_li =[]
    for i in range(0,len(values)):
        dict_li.append({"title":values[i].title, "description":values[i].description,"created_at":values[i].created_at})
    if len(dict_li)==0:
        return jsonify("알림 내역이 없습니다! 곧 좋은 추천 알려드릴게요!")
    else:
        return jsonify(dict_li)


specs_dict = PostAlert().specs_dict
@app.route('/alerts/<userid>',methods = ['POST'])  
@swag_from(specs_dict)
def postAlert(userid):

    values = StylerAlert.query.all().id
    val_len = len(values) + 1
    
    re = request.get_json()
    result = StylerAlert(id=val_len, user_id=userid, title=re['title'], description=re['description']).create()
    # db.session.commit()

    return 'Success!'
    

specs_dict = Water().specs_dict
@app.route('/styler/water/<userid>',methods = ['GET'])  
@swag_from(specs_dict)
def water(userid):
    waterState = Styler.query.filter(Styler.id==userid).first().water_percentage
    if waterState >= 100:
        des = '물통에 물이 너무 많아서 스타일러 가동이 중단되었습니다. 스타일러 물통을 확인해주세요!'
        alert = StylerAlert(user_id = userid, title = "스타일러 상태", description = des)
        db.session.commit
    if waterState <= 10:
        des = '물이 부족합니다! 물을 채워주세요!'
        alert = StylerAlert(user_id = userid, title = "스타일러 상태", description = des)
        db.session.commit

    return jsonify(des)


## 테스트 필요
specs_dict = ScheduleAlert().specs_dict
@app.route('/schedule/<userid>',methods = ['GET'])  
@swag_from(specs_dict)
def scheduleAlert(userid):
    now = datetime.datetime.today().strftime('%y-%m-%d')
    cal = calendar()
    cal = json.loads(cal)
    cal_li = cal['items'][0:]
    todo = '일정이 없습니다.'
    des = '오늘은 일정이 없습니다.'
    for i in range(0,len(cal_li)):
        if cal_li[i]['start'] == now:
            todo = cal_li[i]['summary']
            des = "오늘은" + todo + "일정이 있습니다."
    alert = StylerAlert(user_id = userid, title = "일정 알림", description = des)
    db.session.commit()

    return jsonify(des)


##### 오늘의 추천(수정중 ....... )
specs_dict = RecomToday().specs_dict
@app.route('/recommand/today/<userid>', methods=['GET'])
@swag_from(specs_dict)
def recommand_today(userid):
    name = User.query.filter_by(id=userid).first().username
    info = weatherinfo('Seoul')
    daily = info['daily'] # 일교차: 1 = 큼 / 0 = 크지 않음
    high_temp = info['high_temp'] # 최고기온
    low_temp = info['low_temp'] # 최저기온
    cal = calendar()
    cal = json.loads(cal)
    cal_li = cal['items'][0:]
    sch_li = [] # 일정 리스트
    sch_date = [] # 일정에 대한 date 리스트
    ## 리스트에 요소 추가
    for i in range(0,len(cal_li)):
        sch_li.append(cal_li[i]['summary']) # 스케쥴 리스트
        sch_date.append(cal_li[i]['start']) # 스케쥴 날짜
    
    
    # 이름, 최고온도, 최저온도, 일교차, 스케쥴 리스트
    result = {
        "name":name,
        "max_temp":high_temp,
        "min_temp":low_temp,
        "daily":daily,
        "schedule":sch_li
    }

    return jsonify(result)


##### 제어추천
specs_dict = ControlRecom().specs_dict
@app.route('/recommands/control/<userid>', methods = ['GET']) 
@swag_from(specs_dict)
def control_recom(userid):
    
    ### recommand_data_set
    recom = {
        '울':['고급의류 코스','섬세건조 코스','스팀살균 코스']
    }
    texture = Clothes.query.filter(Clothes.user_id == userid).first().texture
    is_inside = Clothes.query.filter((Clothes.user_id == userid) & (Clothes.is_inside_styler==1)).first().name
    temp = Styler.query.filter(Styler.id == userid).first().temperature
    data = { 
    "userid": int(userid),
    "username": User.query.filter_by(id=userid).first().username,
    "is_inside_styler" : is_inside,
    "texture" : texture,
    "course" : recom[texture],
    "indoor_temp" : temp
    }

    ### styler_alert ###
    # now = datetime.today().strftime('%y-%m-%d %H:%M:%S')
    des = recom[texture][0] + "을(를) 추천합니다" ## 수정필요
    alert = StylerAlert(user_id = userid, title = "제어 추천", description = des)
    db.session.commit()

    return jsonify(data)



###### Styler Part

### 스타일러 상태 조회
specs_dict = CheckStylerState().specs_dict
@app.route('/state/stylers/<userid>',methods = ['GET'])
@swag_from(specs_dict)
def check_state(userid):
    new_control = Control.query.filter(Control.id==userid).first()
    
    ## 스타일러 가동 중
    if (new_control.ready+new_control.refresh+new_control.dry) > 0:
        turn_on = 1

        ### styler_alert ###
        # now = datetime.today().strftime('%y-%m-%d %H:%M:%S')
        des = "스타일러가 가동 중입니다."
        alert = StylerAlert(user_id = userid, title = "스타일러 상태", description = des)
        db.session.commit()
    
    ## 스타일러 가동 X
    else:
        turn_on = 0
    conn_dict = {"styler_connection" : Styler.query.filter(Styler.id ==userid).first().connection, "mirror_connection" : Mirror.query.filter(Mirror.id==userid).first().connection, "turn_on":turn_on}
    new_control = Control.query.filter(Control.id==userid).first()
    schema = controlSchema(only=("reserv","ready","refresh","dry"))
    result = schema.dump(new_control)
    result = {**conn_dict, **result}
    return result


### 스타일러 모드 변경(업데이트)
specs_dict = ControlStyler().specs_dict
@app.route('/state/stylers/<userid>',methods = ['PATCH'])
@swag_from(specs_dict)
def control_styler(userid):
    mode = request.get_json()["mode"]
    new_styler = Styler.query.filter(Styler.id ==1).first()
    new_control = Control.query.filter(Control.id==1).first()
    schema_sty = stylerSchema()
    schema_con = controlSchema()
    result_con = schema_con.dump(new_control)
    result = schema_sty.dump(new_styler)
    c = Counter(result_con.values())
    
    ## 스타일러 연결 상태 체크
    if result['connection'] == 1:
        ##  counter로 1의 갯수를 세서, 기능이 모두 off 일때만 새로운 기능을 on 할 수 있도록
        ## ex. id는 무조건 1이상이므로, 예약을 포함한 작동 중 기능 모두 꺼져 있어야 함
        ## 다만, 자동건조와, 자동제습은 제외
        if c[1] - (new_control.indoor_dehumification+new_control.autodry) < 2:
            ## 스타일러 모드를 받아와서 실행시킬 모드를 1로 turn on하고 db에 상태 저장
            new_control.data = {mode : 1}
            Control.query.filter_by(id=userid).update(new_control.data)
            db.session.commit()
            # update_schema = schema_con.dump(new_control)
            
            ## restful_api로 상태 반환
            # return update_schema
            return 'update 완료!'
        else:
            return '현재 스타일러가 실행 중입니다!'
    else:
        return '스타일러 연결에 실패하였습니다.'

#### 내옷장 Part  
specs_dict = NeedStyler().specs_dict
@app.route('/recommand/styler/<clothes>/<userid>',methods = ['GET'])
@swag_from(specs_dict)
def need_styler(clothes,userid):
    cal = calendar()
    cal = json.loads(cal)
    cal_li = cal['items'][0:]
    sch_li = [] # 일정 리스트
    sch_date = [] # 일정에 대한 date 리스트
    
    ## 리스트에 요소 추가
    for i in range(0,len(cal_li)):
        sch_li.append(cal_li[i]['summary'])
        sch_date.append(cal_li[i]['start'])
        
    # 일정에 대한 dict 만들기    
    sch_dict = dict(zip(sch_li,sch_date))
    
    new_clothes = Clothes.query.filter(Clothes.name ==clothes).first()
    schema = clotheSchema()
    clo_json = schema.dump(new_clothes)
    last_time = datetime.date.today() - datetime.date(int(clo_json['stylered_at'][0:4]),int(clo_json['stylered_at'][5:7]),int(clo_json['stylered_at'][8:10])) # 마지막 스타일러 가동으로부터 지난 시간
    
    
    #### 추천 알고리즘(일정 & 마지막 스타일러 가동날짜를 고려한)
    timedel = np.timedelta64(last_time,'ns')
    day = timedel.astype('timedelta64[D]')
    day = day.astype(int)
    
    # 데이터 셋을 통해 학습
    standard = control_csv(clothes,userid)
    print(type(standard))
    if len(standard) != 0:
        event_date = sch_dict[standard[0]]['date']   
        new_timedel =  datetime.date(int(event_date[0:4]),int(event_date[5:7]),int(event_date[8:10])) - datetime.date.today()
        new_timedel = np.timedelta64(new_timedel,'ns')
        new_day = new_timedel.astype('timedelta64[D]')
        new_day = new_day.astype(int)
        df = pd.read_csv('flaskr/dataset.csv')
        df = pd.DataFrame(df) 
        for i in range(0,min(len(df[clothes].tolist()),len(sch_li))):
            if (sch_li[i] in df[clothes].tolist()) == True :
                testing = 1 # 캘린더에 요청한 옷에 관한 스케쥴이 존재
                break
            else :
                testing = 0 # 캘린더에 요청한 옷에 관한 스케쥴 X
            
        if testing == 1:
            tm = 2*day + np.exp2(6-new_day) # 기준 함수
            ### need_styler_set : 0 = 매우필요 1 = 필요 2 = 괜찮음
            if tm >= 8:
                need_styler_set = 0 # 매우 필요
            
            elif tm >= 6 and tm < 8:
                need_styler_set = 1 # 필요
            
            else :
                need_styler_set = 2 # 괜찮음

        elif testing == 0:
            tm = 2*day + np.exp2(6-new_day) # 기준 함수 
            if tm >= 8:
                need_styler_set = 0 # 매우 필요
            
            elif tm >= 6 and tm < 8:
                need_styler_set = 1 # 필요
            
            else :
                need_styler_set = 2 # 괜찮음


        # need_styler update
        new_clothes.need_styler = need_styler_set
        db.session.commit()
        result = schema.dump(new_clothes)
        return result
    else:
        result = schema.dump(new_clothes)
        return result


## 내 옷장 조회
specs_dict = Closet().specs_dict
@app.route('/users/clothes/<userid>', methods=['GET'])
@swag_from(specs_dict)
def check_closet(userid):
    closet = Clothes.query.filter(Clothes.user_id == userid).all()
    dict_li = []
    for i in range(0,len(closet)):
        dict_li.append({"id":closet[i].id, "name":closet[i].name, "need_styler":closet[i].need_styler, "is_inside_styler":closet[i].is_inside_styler, "created_at":closet[i].created_at, "stylered_at":closet[i].stylered_at, "color:":closet[i].color,"texture":closet[i].texture,"clothe_type":closet[i].clothes_type.name,"sub_type":closet[i].sub_type})
    for i in range(0,len(dict_li)):
        need_styler(dict_li[0]['name'],userid)
    return jsonify(dict_li)



## 내 옷장에 새 옷 등록(Add clothes)
specs_dict = AddClothes().specs_dict
@app.route('/users/clothes/<userid>',methods = ['POST'])
@swag_from(specs_dict)
def add_clothes(userid):
    json_data = request.get_json()
    schema = clotheSchema(only=("name","user_id","clothes_type","sub_type","color","texture"))
    new_clothe_data = Clothes(name= json_data['name'],user_id=userid, clothes_type= json_data['category'], sub_type= json_data['sub_type'], color= json_data['color'], texture= json_data['texture'] ).create()
    result = schema.dump(new_clothe_data)
    return result


specs_dict = Weather().specs_dict
@app.route('/weather/<city>', methods=['GET'])
@swag_from(specs_dict)
def weatherinfo(city):
    schema = weatherSchema()
    weather = getWeather(city)
    high_temp = float(weather['main']['temp_max'])-273.15 # 절대온도 -> 섭씨 변환
    low_temp = float(weather['main']['temp_min'])-273.15 ## 온도 더블 체크하기
    if high_temp-low_temp > 10 : # 일교차가 클 경우(기준: 10도)
            daily = 1
            temp_data = {
                "high_temp":high_temp,
                "low_temp":low_temp,
                "daily":daily
            }
            result = schema.dump(temp_data)
    else : # 일교차가 크지 않을 경우
            daily = 0   
            temp_data = {
                "high_temp":high_temp,
                "low_temp":low_temp,
                "daily":daily
            }
            result = schema.dump(temp_data)
    return result
        



@app.route('/')
def root():
    return '<h1>Welcome to ms-tromm API</h1>'



### error handler ###
@app.errorhandler(HTTPException)
def error_handler(e):
    response = e.get_response()

    response.data = json.dumps({
        'code': e.code,
        'msg' : e.name,
        'desc': e.description,
    })
    response.content_type = 'application/json'
    return response




def control_csv(clothe, userid):
    data = pd.read_csv('flaskr/dataset.csv')
    data = pd.DataFrame(data)   
    cal = calendar()
    cal = json.loads(cal)
    cal_li = cal['items'][0:]
    sch_li = [] # 일정 리스트
    sch_date = [] # 일정에 대한 date 리스트
    match_li = []
    to_update = []
    
    ## 리스트에 요소 추가
    for i in range(0,len(cal_li)):
        sch_li.append(cal_li[i]['summary'])
        sch_date.append(cal_li[i]['start'])
    
    dataf = data[clothe].dropna(how='any').tolist()
    new_sch_li = [i.replace(' ',' ') for i in sch_li]
    for i in range(0,min(len(dataf),len(new_sch_li))):
        if (new_sch_li[i] in dataf) == True:
            match_li.append(new_sch_li[i])
        else:
            to_update.append(new_sch_li[i])
    
    new_sch_count = Schedule.query.filter_by(user_id=userid).first()
    ### DB 비어있는지 확인
    if type(new_sch_count) == type(None): 
        for i in range(0, len(to_update)):
            new_schdule = Schedule(id = i+1, cont = i+1, user_id=userid, title=to_update[i], description=to_update[i]).create()                          
    return match_li
        
    
    
    
### 유저를 통해 학습하는 func  
specs_dict = AddCSV().specs_dict
@app.route('/clothe/schedule/<userid>', methods = ['POST'])
@swag_from(specs_dict)
def add_csv(userid):
    data = request.get_json()
    
    for i in range(0,len(data)):
        need_styler(data[i]['clothes'],userid)
    dataFrame = pd.read_csv('flaskr/dataset.csv')
    dataFrame = pd.DataFrame(dataFrame)
    data_dict = dataFrame.to_dict()
    
    ### 학습 데이터 셋(csv) 업데이트를 위한 딕셔너리
    for i in range(0,len(data)):
        target_num = max(list(data_dict[data[i]['clothes']].keys()))+1
        target  = data[i]['clothes']
        data_dict[list(data[i].values())[i]].update({target_num:target}) 
    
    # Dict -> CSV 
    new_df = pd.DataFrame(data_dict)
    new_df.to_csv('flaskr/dataset.csv')
  
  
    # 학습을 끝난 데이터는 DB에서 삭제
    Schedule.query.filter(Schedule.user_id == userid).delete()
    db.session.commit()
    return 'finish update!'


##### 오늘의 추천 
specs_dict = TodayRecom().specs_dict
@app.route('/recommend/today/<city>/<userid>', methods = ['GET'])
@swag_from(specs_dict)
def recommendToday(city, userid):
    items = getWeather(city)
    temp = items['main']['temp']-273.15
    
    dataFrame = pd.read_csv('flaskr/clothe.csv')
    dataFrame = pd.DataFrame(dataFrame)
    data_dict = dataFrame.to_dict()

    key = 0    
    for i in range(7):
        if int(temp) > int(data_dict['low_temp'][i]) and int(temp) < int(data_dict['high_temp'][i]):
            key = i
            break

    today = datetime.datetime.today().strftime('%m')
    if today in [3,4,5]:
        season = "봄"
    elif today in [6,7,8]:
        season = "여름"
    elif today in [9,10,11]:
        season = "가을"
    else:
        season = "겨울"

    result = {
        "top" : data_dict['top'][key],
        "down" : data_dict['down'][key],
        "scent" : Scent.query.filter(Scent.description==season).first().name
    }

    ### styler_alert ###
    # now = datetime.today().strftime('%y-%m-%d %H:%M:%S')
    des = "오늘의 추천은"+result['top']+"와(과)"+result['down']+", 그리고"+result['scent']+"입니다."
    alert = StylerAlert(user_id = userid, title = "오늘의 추천", description = des)
    db.session.commit()

    return jsonify(result)

