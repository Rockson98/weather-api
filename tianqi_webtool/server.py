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
                "url": "https://weather-api-d7j0.onrender.com",
                "description": "Render生产服务器"
            },
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
                                   "description": "城市名称（支持中文、英文或中英文混合，如：北京、Beijing、New York、纽约等）",
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
                                            "feels_like": {
                                                "type": "number",
                                                "description": "体感温度（摄氏度）"
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
        print(f"Received city parameter: {city}")  # 调试信息
        # 从环境变量获取API密钥，如果未设置则使用默认值
        api_key = os.getenv('WEATHER_API_KEY', '811a271ed44e1d5599d8e0c773417557')
        
        if not api_key:
            return jsonify({"error": "API密钥未配置"}), 500
        
        # 城市名映射（可选，用于常见城市的中英文转换）
        city_mapping = {
            '北京': 'Beijing',
            '上海': 'Shanghai',
            '广州': 'Guangzhou',
            '深圳': 'Shenzhen',
            '杭州': 'Hangzhou',
            '南京': 'Nanjing',
            '成都': 'Chengdu',
            '武汉': 'Wuhan',
            '西安': 'Xian',
            '重庆': 'Chongqing',
            '天津': 'Tianjin',
            '苏州': 'Suzhou',
            '青岛': 'Qingdao',
            '大连': 'Dalian',
            '厦门': 'Xiamen',
            '福州': 'Fuzhou',
            '济南': 'Jinan',
            '郑州': 'Zhengzhou',
            '长沙': 'Changsha',
            '昆明': 'Kunming',
            '贵阳': 'Guiyang',
            '兰州': 'Lanzhou',
            '银川': 'Yinchuan',
            '西宁': 'Xining',
            '乌鲁木齐': 'Urumqi',
            '拉萨': 'Lhasa',
            '呼和浩特': 'Hohhot',
            '石家庄': 'Shijiazhuang',
            '太原': 'Taiyuan',
            '沈阳': 'Shenyang',
            '长春': 'Changchun',
            '哈尔滨': 'Harbin',
            '合肥': 'Hefei',
            '南昌': 'Nanchang',
            '南宁': 'Nanning',
            '海口': 'Haikou',
            '三亚': 'Sanya'
        }
        
        # 智能城市名处理
        # 1. 如果输入的是中文城市名且在映射表中，使用英文名
        # 2. 如果输入的是英文城市名或不在映射表中，直接使用原输入
        # 3. 支持中英文混合查询
        if city in city_mapping:
            query_city = city_mapping[city]
            print(f"使用映射的城市名: {city} -> {query_city}")
        else:
            query_city = city
            print(f"直接使用输入的城市名: {query_city}")
        
        print(f"最终查询城市: {query_city}")  # 调试信息
        
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': query_city,
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
            "feels_like": data['main']['feels_like'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
