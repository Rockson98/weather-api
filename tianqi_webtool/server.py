   from flask import Flask, request, jsonify
   import requests
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   app = Flask(__name__)
   
   @app.route('/')
   def home():
       return jsonify({"message": "天气API服务正在运行"})
   
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
