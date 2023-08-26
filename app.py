import requests
from flask import Flask, render_template, jsonify, request, g
from flask_paginate import Pagination

app = Flask(__name__)



@app.before_request
def load_data():
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/Perseverance/latest_photos?api_key=gXgqmDNzfhzkFhzYIRBzGzIqmbTuKItwLXq2cVcW'
    response = requests.get(url)
    if response.status_code == 200:

        g.data = response.json()


@app.route('/')
def index():
    if hasattr(g, 'data'):
        # Разбиваем данные на страницы по 6 элементов на каждой
        page = request.args.get('page', type=int, default=1)
        per_page = 6
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        photos = g.data['latest_photos'][start_idx:end_idx]

        total_photos = len(g.data['latest_photos'])

        # Создаем объект пагинации
        pagination = Pagination(page=page, total=total_photos, per_page=per_page, bs_version=4)

        return render_template("index.html", photos=photos, pagination=pagination)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
