from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域请求
   
@app.route('/')
def home():
    return jsonify({"message": "天气API服务正在运行"})

@app.route('/openapi.json')
def openapi():
    """返回OpenAPI规范文档"""
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "天气API服务",
            "description": "提供天气查询功能的API服务",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "http://localhost:8000",
                "description": "本地开发服务器"
            }
        ],
        "paths": {
            "/weather": {
                "get": {
                    "summary": "获取天气信息",
                    "description": "根据城市名称获取当前天气信息",
                    "operationId": "getWeather",
                    "parameters": [
                        {
                            "name": "city",
                            "in": "query",
                            "description": "城市名称",
                            "required": True,
                            "schema": {
                                "type": "string",
                                "example": "北京"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "成功获取天气信息",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "city": {
                                                "type": "string",
                                                "description": "城市名称"
                                            },
                                            "temperature": {
                                                "type": "number",
                                                "description": "温度（摄氏度）"
                                            },
                                            "description": {
                                                "type": "string",
                                                "description": "天气描述"
                                            },
                                            "humidity": {
                                                "type": "number",
                                                "description": "湿度（百分比）"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "服务器错误",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {
                                                "type": "string",
                                                "description": "错误信息"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    })
   
   @app.route('/weather', methods=['GET'])
   def get_weather():
       try:
           city = request.args.get('city', '北京')
           api_key = os.getenv('WEATHER_API_KEY')
           
           if not api_key:
               return jsonify({"error": "API密钥未配置"}), 500
           
           url = f"https://api.openweathermap.org/data/2.5/weather"
           params = {
               'q': city,
               'appid': api_key,
               'units': 'metric',
               'lang': 'zh_cn'
           }
           
           response = requests.get(url, params=params)
           response.raise_for_status()
           
           data = response.json()
           return jsonify({
               "city": data['name'],
               "temperature": data['main']['temp'],
               "description": data['weather'][0]['description'],
               "humidity": data['main']['humidity']
           })
           
       except Exception as e:
           return jsonify({"error": str(e)}), 500
   
   if __name__ == "__main__":
       app.run(debug=True)
