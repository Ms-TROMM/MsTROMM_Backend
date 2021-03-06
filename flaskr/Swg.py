from flasgger import swag_from
from flask import Flask, jsonify
from flasgger import Swagger


class Status:
    specs_dict = {
    "parameters" : [
        {
        "name" : "device",
        "in" : "path",
        "type" : "string",
        "required" : "true",
        "default" : "styler"
        }
    ],
    "definitions" : {
        "DeviceStatus" : {
        "type": "object",
        "properties" : {
            "connection": {
                "type" : "integer",
            },
            "id":{
                "type" : "integer",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "Show device status",
        "schema": {
            "$ref": '#/definitions/DeviceStatus', 
            },
        "examples": {
            "connection" : 0,
            "id" : 1
        }
        }
    }
    }
    

class Standard:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "Username": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
            }
        }
        },
    },
    #### 왜 example 안나옴?
    "responses": {
    "200": {
        "description": "Show username",
        "schema": {
            "$ref": '#/definitions/Username', 
            },
        "examples": {
            "username" : "kim"
        }
        }
    }
    }


class HomeInfo:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        },
        {
        "name": "city",
        "in": "path",
        "type": "string",
        "required": "true",
        "default": "Seoul"
        }
    ],
    "definitions" : {
        "HomeInfo": {
        "type": "object",
        "properties": {
            "dehumification_connect": {
                "type": "integer",
            },
            "dry_connection": {
                "type": "integer",
            },
            "indoor_humidity": {
                "type": "integer",
            },
            "indoor_temp": {
                "type": "integer",
            },
            "max_temp": {
                "type": "integer",
            },
            "min_temp": {
                "type": "integer",
            },
            "mirror_connection": {
                "type": "integer",
            },
            "now_mode": {
                "type": "string",
            },
            "now_temp": {
                "type": "integer",
            },
            "styler_connection": {
                "type": "integer",
            },
            "styler_water": {
                "type": "integer",
            },
            "todya_date": {
                "type": "string",
            },
            "today_week": {
                "type": "string",
            },
            "userid": {
                "type": "integer",
            },
            "username": {
                "type": "string",
            },
        }
        },
    },
    "responses": {
    "200": {
        "description": "홈-1~4 관련",
        "schema": {
            "$ref": '#/definitions/HomeInfo', 
            },
        "examples": {
            "dehumification_connect" : 0,
            "dry_connect" : 0,
            "indoor_humidity" : 60,
            "indoor_temp" : 22,
            "max_temp" : 10,
            "min_temp" : 8,
            "mirror_connection" : 0,
            "now_mode" : "리프레쉬",
            "now_temp" : 10,
            "styler_connection" : 1,
            "styler_water" : 100,
            "today_date" : "06",
            "today_week" : "월",
            "userid" : 1,
            "username" : "김엘지"
        }
        }
    }
    }


class ControlRecom:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": "1"
        }
    ],
    "definitions" : {
        "ControlRecom": {
        "type": "object",
        "properties": {
            "course": {
                "type": "list", ## 오류...
            },
            "indoor_temp": {
                "type": "string",
            },
            "is_inside_styler": {
                "type": "string",
            },
            "texture": {
                "type": "string",
            },
            "useid": {
                "type": "integer",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "추천(제어 추천) 관련",
        "schema": {
            "$ref": '#/definitions/ControlRecom', 
            },
        "examples": {
            "course" : ["고급의류 코스", "섬세건조 코스", "스팀살균 코스"],
            "indoor_temp" : 22,
            "is_inside_styler" : "정장1",
            "texture" : "울",
            "userid" : 1
        }
        }
    }
    }


class CheckStylerState:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "CheckStylerState": {
        "type": "object",
        "properties": {
            "dry": {
                "type": "integer",
            },
            "mirror_connection": {
                "type": "integer",
            },
            "ready": {
                "type": "integer",
            },
            "refresh": {
                "type": "integer",
            },
            "reserv": {
                "type": "integer",
            },
            "styler_connection": {
                "type": "integer",
            },
            "turn_on": {
                "type": "integer",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "스타일러 ~ 스타일러-3 관련",
        "schema": {
            "$ref": '#/definitions/CheckStylerState', 
            },
        "examples": {
            "dry" : 0,
            "mirror_connection" : 0,
            "ready" : 0,
            "refresh" : 0,
            "reserv" : 0,
            "styler_connection" : 1,
            "turn_on" : 0
        }
        }
    }
    }


## 수정필요 (example 포멧 수정...)
class Closet:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "Closet": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
            },
            "is_inside_styler": {
                "type": "integer",
            },
            "name": {
                "type": "string",
            },
            "need_styler": {
                "type": "integer",
            },
            "clothe_type":{
                "type":"string"
            },
            "color":{
                "type":"integer"
            },
            "created_at":{
                "type":"datetime"
            },
            "stylered_at":{
                "type":"datetime"
            },
            "sub_type":{
                "type":"integer"
            },
            "texture":{
                "type":"string"
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "내 옷장 관련, 내 옷장에 모든 옷들 상태를 리스트로 반환[{}]",
        "schema": {
            "$ref": '#/definitions/Closet', 
            },
        "examples": {
        "clothe_type": "top",
        "color:": 212121,
        "created_at": "Wed, 10 Nov 2021 13:44:33 GMT",
        "id": 3,
        "is_inside_styler": 0,
        "name": "티셔츠",
        "need_styler": 0,
        "stylered_at": "Sat, 20 Nov 2021 13:44:33 GMT",
        "sub_type": 1,
        "texture": "soft"
    }
        }
    }
    }


class Weather:
    specs_dict = {
    "parameters": [
        {
        "name": "city",
        "in": "path",
        "type": "string",
        "required": "true",
        "default": "Seoul"
        }
    ],
    "definitions" : {
        "Weather": {
        "type": "object",
        "properties": {
            "daily": {
                "type": "integer",
            },
            "high_temp": {
                "type": "integer",
            },
            "low_temp": {
                "type": "integer",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "Show Weather Information",
        "schema": {
            "$ref": '#/definitions/Weather', 
            },
        "examples": {
            "daily" : 0,
            "high_temp" : 9,
            "low_temp" : 8
        }
        }
    }
    }


class TodayRecom:
    specs_dict = {
    "parameters": [
        {
        "name": "city",
        "in": "path",
        "type": "string",
        "required": "true",
        "default": "Seoul"
        },
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "TodayRecom": {
        "type": "object",
        "properties": {
            "down": {
                "type": "string",
            },
            "scent": {
                "type": "string",
            },
            "top": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "추천(오늘의 추천)에서 옷 관련(ex. 두꺼운 가디건, 활동성..., 민트향)",
        "schema": {
            "$ref": '#/definitions/TodayRecom', 
            },
        "examples": {
            "down" : "청바지",
            "scent" : "musk",
            "top" : "패딩"
        }
        }
    }
    }


class AddPrefer:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "AddPrefer": {
        "type": "object",
        "properties": {
            "scentid_one": {
                "type": "string",
            },
            "scentid_two": {
                "type": "string",
            },
            "scentid_three": {
                "type": "string",
            },
            "fashion_one": {
                "type": "string",
            },
            "fashion_two": {
                "type": "string",
            },
            "fashion_three": {
                "type": "string",
            },
            "color_one": {
                "type": "string",
            },
            "color_two": {
                "type": "string",
            },
            "color_three": {
                "type": "string",
            }       
        }
        },
    },
    "responses": {
    "200": {
        "description": "설문지-1~6관련",
        "schema": {
            "$ref": '#/definitions/AddPrefer', 
            },
        "examples": {
            "scentid_one" : "woody",
            "scentid_two" : "citrus",
            "scentid_three" : "green",
            "fashion_one" : "relax",
            "fashion_two" : "coat",
            "fashion_three" : "clean",
            "color_one" : "green",
            "color_two" : "yellow",
            "color_three" : "ivory"
        }
        }
    }
    }


class AddClothes:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "AddClothes": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "category": {
                "type": "string",
            },
            "subtype": {
                "type": "integer",
            },
            "color": {
                "type": "integer",
            },
            "texture": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "새 옷 등록하기 관련",
        "schema": {
            "$ref": '#/definitions/AddClothes', 
            },
        "examples": {
            "name" : "정장1",
            "categpry" : "onepiece",
            "sub_type" : 3,
            "color" : 292929,
            "texture" : "울"
        }
        }
    }
    }


class ControlStyler:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "ControlStyler": {
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "스타일러에서 버튼(ex. 살균~섬세건조) 눌렀을 때, mode (상태) 변경",
        "schema": {
            "$ref": '#/definitions/ControlStyler', 
            },
        "examples": {
            "mode" : "리프레쉬"
        }
        }
    }
    }


class AddCSV:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "AddCSV": {
        "type": "object",
        "properties": {
            "schedule": {
                "type": "string",
            },
            "clothes": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "학습 팝업 관련",
        "schema": {
            "$ref": '#/definitions/AddCSV', 
            },
        "examples": {
            "schedule" : "LG전자면접",
            "clothes" : "정장"
        }
        }
    }
    }


class RecomToday:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "RecomToday": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "max_temp": {
                "type": "integer",
            },
            "min_temp": {
                "type": "integer",
            },
            "daily": {
                "type": "integer",
            },
            "schedule": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "추천(오늘의 추천) 관련",
        "schema": {
            "$ref": '#/definitions/RecomToday', 
            },
        "examples": {
            "name" : "김엘지",
            "max_temp" : 13,
            "min_temp" : 7,
            "daily" : 6,
            "schedule" : "LG전자 면접"
        }
        }
    }
    }


class NeedStyler:
    specs_dict = {
    "parameters": [
        {
        "name": "clothes",
        "in": "path",
        "type": "string",
        "required": "true",
        "default": "티셔츠"
        },
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "NeedStyler": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "내옷장 - 스타일러 필요도 관련",
        "schema": {
            "$ref": '#/definitions/NeedStyler', 
            },
        "examples": {
            "name" : "김엘지"
        }
        }
    }
    }
    

class Water:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "Water": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "제어추천팝업, 제어추천팝업1 관련",
        "schema": {
            "$ref": '#/definitions/Water', 
            },
        "examples": {
            "description" : "물이 부족합니다! 물을 채워주세요!"
        }
        }
    }
    }


class ScheduleAlert:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "ScheduleAlert": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "일정추천팝업",
        "schema": {
            "$ref": '#/definitions/ScheduleAlert', 
            },
        "examples": {
            "description" : "오늘은 LG전자 면접이 있습니다."
        }
        }
    }
    }


class Alert:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "Alert": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            },
            "description": {
                "type": "string",
            },
            "created_at": {
                "type": "string"
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "알림-푸시알림설정전, 알림-알림없을시, 알림-1, 알림-2, 알림-3 관련",
        "schema": {
            "$ref": '#/definitions/Alert', 
            },
        "examples": {
            "title" : "오늘의 알림",
            "description" : "오늘은 LG전자 면접이 있습니다.",
            "created_at" : "2021-12-03 03:39:27"
        }
        }
    }
    }

class PostAlert:
    specs_dict = {
    "parameters": [
        {
        "name": "userid",
        "in": "path",
        "type": "integer",
        "required": "true",
        "default": 1
        }
    ],
    "definitions" : {
        "PostAlert": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            },
            "description": {
                "type": "string",
            }
        }
        },
    },
    "responses": {
    "200": {
        "description": "알림-푸시알림설정전, 알림-알림없을시, 알림-1, 알림-2, 알림-3 관련",
        "schema": {
            "$ref": '#/definitions/PostAlert', 
            },
        "examples": {
            "title" : "오늘의 알림",
            "description" : "오늘은 LG전자 면접이 있습니다.",
        }
        }
    }
    }