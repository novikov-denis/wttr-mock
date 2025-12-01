from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import random

# Координаты городов и примерные диапазоны температур
CITIES_DATA = {
    'омск': {'temp': (-25, 5), 'wind': (2, 10)},
    'калининград': {'temp': (-5, 10), 'wind': (3, 12)},
    'челябинск': {'temp': (-25, 5), 'wind': (2, 8)},
    'владивосток': {'temp': (-15, 5), 'wind': (4, 15)},
    'красноярск': {'temp': (-30, 0), 'wind': (1, 8)},
    'москва': {'temp': (-15, 5), 'wind': (2, 10)},
    'екатеринбург': {'temp': (-25, 3), 'wind': (2, 9)},
    'moscow': {'temp': (-15, 5), 'wind': (2, 10)},
    'london': {'temp': (0, 15), 'wind': (3, 12)},
    'paris': {'temp': (0, 15), 'wind': (2, 10)},
}

WEATHER_EMOJIS = ['☀️', '⛅', '☁️', '🌧️', '🌦️', '❄️', '🌫️', '🌤️']


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path).strip('/').lower()
        
        # Убираем "api/" если есть
        if path.startswith('api/'):
            path = path[4:]
        
        # Город по умолчанию
        city = path if path else 'москва'
        
        # Получаем данные города или используем дефолтные
        city_data = CITIES_DATA.get(city, {
            'temp': (-10, 10), 'wind': (1, 10)
        })
        
        # Генерируем погоду (с seed для воспроизводимости в течение часа)
        from datetime import datetime
        hour_seed = datetime.now().strftime("%Y%m%d%H")
        random.seed(hash(city + hour_seed))
        
        temp = random.randint(city_data['temp'][0], city_data['temp'][1])
        wind = round(random.uniform(city_data['wind'][0], city_data['wind'][1]), 1)
        emoji = random.choice(WEATHER_EMOJIS)
        
        # Формируем ответ в формате wttr.in (format=2)
        temp_str = f'+{temp}' if temp >= 0 else str(temp)
        response_text = f'{emoji} 🌡️{temp_str}°C 🌬️↑{wind}m/s\n'
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response_text.encode('utf-8'))
        return
