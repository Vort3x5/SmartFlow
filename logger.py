import time
import subprocess
from tinydb import TinyDB
from datetime import datetime

db = TinyDB('/home/doniczka/app/db.json')

def get_moisture():
    try:
        result = subprocess.run(['/home/doniczka/app/sensor'], capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 0.0

while True:
    moisture = get_moisture()
    timestamp = datetime.now().isoformat()
    db.insert({'time': timestamp, 'moisture': moisture})
    time.sleep(300) # Rejestracja co 300 sekund (5 minut)
