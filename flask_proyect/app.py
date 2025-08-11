
from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_folder='assets')

CHARACTER_API_URL = 'https://rickandmortyapi.com/api/character'
EPISODE_API_URL = 'https://rickandmortyapi.com/api/episode'

# Página de inicio
@app.route('/')
def inicio():
    return render_template('index.html', active='inicio')

# Página de personajes
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

# Página de episodios
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
    app.run(debug=True, host='0.0.0.0')
