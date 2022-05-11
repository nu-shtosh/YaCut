# yacut/api_views.py
import re

from flask import jsonify, request
from http import HTTPStatus
from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    '''POST метод, создание ссылки'''
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    short_name = data.get('custom_id')
    if short_name == '' or short_name is None:
        short_name = get_unique_short_id()


    SYMBOLS = '^[A-Za-z0-9]*$'
    APPROVED_SYMBOLS = re.match(SYMBOLS, short_name)

    if short_name:
        if len(short_name) > 6:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URL_map.query.filter_by(short=short_name).first():
            raise InvalidAPIUsage(f'Имя "{short_name}" уже занято.')
        if not APPROVED_SYMBOLS:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map = URL_map(
        original=data.get('url'),
        short=short_name
    )
    db.session.add(url_map)
    db.session.commit()
    return (jsonify(url_map.to_dict()), HTTPStatus.CREATED)


@app.route('/api/id/<string:short>/')
def get_full_url_api(short):
    '''GET метод, получение определленого id'''
    url_map = URL_map.query.filter_by(short=short).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return (jsonify(url_map.only_url_to_dict()), HTTPStatus.OK)
