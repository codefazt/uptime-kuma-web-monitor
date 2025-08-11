from flask import Flask, render_template, request, redirect, url_for
from flask_apscheduler import APScheduler
import requests
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='assets')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'novedades.log')
LAST_ID_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'last_id.json')
UPTIME_KUMA_PUSH_URL = 'http://uptime-kuma:3001/api/push/Y9UM7SAGUc?status=up&msg=OK&ping='
CHARACTER_API_URL = 'https://rickandmortyapi.com/api/character'
EPISODE_API_URL = 'https://rickandmortyapi.com/api/episode'

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

job_enabled = True  # Estado del job

# Utilidad para leer el último ID
def get_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, 'r') as f:
            try:
                return json.load(f).get('last_id', 0)
            except Exception:
                return 0
    return 0

def set_last_id(last_id):
    with open(LAST_ID_FILE, 'w') as f:
        json.dump({'last_id': last_id}, f)

# Job programado
def novedades_job():
    try:
        response = requests.get(CHARACTER_API_URL)
        response.raise_for_status()
        data = response.json()
        personajes = data.get('results', [])
        last_id = get_last_id()
        nuevos = [p for p in personajes if p['id'] > last_id]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if nuevos:
            nombres = ', '.join([p['name'] for p in nuevos])
            log_msg = f"[{now}] Se encontraron {len(nuevos)} nuevos personajes: {nombres}\n"
            set_last_id(max(p['id'] for p in nuevos))
        else:
            log_msg = f"[{now}] No hay novedades\n"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg)
        # Push a Uptime Kuma
        requests.get(UPTIME_KUMA_PUSH_URL)
    except Exception as e:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{now}] Error: {str(e)}\n"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg)

# Registrar el job
scheduler.add_job(id='novedades_job', func=novedades_job, trigger='interval', minutes=1)

@app.route('/')
def index():
    return render_template('index.html', active='inicio')

@app.route('/novedades')
def novedades():
    # Paginación básica
    page = int(request.args.get('page', 1))
    per_page = 10
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = f.readlines()
    logs = logs[::-1]  # Mostrar lo más reciente primero
    total = len(logs)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_logs = logs[start:end]
    has_next = end < total
    has_prev = start > 0
    return render_template('informe_novedades.html', logs=paginated_logs, page=page, has_next=has_next, has_prev=has_prev, job_enabled=job_enabled)

@app.route('/toggle-job', methods=['POST'])
def toggle_job():
    global job_enabled
    job_enabled = not job_enabled
    if job_enabled:
        scheduler.resume_job('novedades_job')
    else:
        scheduler.pause_job('novedades_job')
    return redirect(url_for('novedades'))

@app.route('/personajes')
def personajes():
    page = int(request.args.get('page', 1))
    params = {'page': page}
    response = requests.get(CHARACTER_API_URL, params=params)
    data = response.json()
    characters = data.get('results', [])
    info = data.get('info', {})
    total_characters = info.get('count', 0)
    total_pages = (total_characters + 8) // 9
    # Mostrar solo 9 personajes por página
    start = ((page - 1) * 9) % 20
    end = start + 9
    characters = characters[start:end]
    return render_template('personajes.html', characters=characters, page=page, total_pages=total_pages, active='personajes')

@app.route('/episodios')
def episodios():
    page = int(request.args.get('page', 1))
    params = {'page': page}
    response = requests.get(EPISODE_API_URL, params=params)
    data = response.json()
    episodios = data.get('results', [])
    info = data.get('info', {})
    total_episodios = info.get('count', 0)
    total_pages = (total_episodios + 8) // 9
    # Mostrar solo 9 episodios por página
    start = ((page - 1) * 9) % 20
    end = start + 9
    episodios = episodios[start:end]
    return render_template('episodios.html', episodios=episodios, page=page, total_pages=total_pages, active='episodios')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
