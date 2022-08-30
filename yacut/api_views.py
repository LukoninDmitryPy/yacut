from http import HTTPStatus
from re import match
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')
    if URL_map.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    url = URL_map(
        original=data.get('url'),
        short=data['custom_id']
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(
            'Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original})
