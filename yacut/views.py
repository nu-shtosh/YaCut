# yacut/views.py
import random
import string
from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URL_map_Form
from .models import URL_map


def get_unique_short_id():
    '''Новое короткое имя.'''
    LOWER_LETTERS = string.ascii_lowercase
    NUMS = string.digits
    UPPER_LETTERS = string.ascii_uppercase
    ALLSYMB = LOWER_LETTERS + NUMS + UPPER_LETTERS
    AMOUNT = 6
    short_name = str(''.join(random.choices(ALLSYMB, k=AMOUNT)))
    if URL_map.query.filter_by(short=short_name).first():
        get_unique_short_id()
    return short_name


@app.route('/', methods=['POST', 'GET'])
def index_view():
    '''Главная страница.'''
    form = URL_map_Form()
    if form.validate_on_submit():
        short_name = form.custom_id.data

        if URL_map.query.filter_by(short=short_name).first():
            flash(f'Имя {short_name} уже занято!')
            return render_template('yacut.html', form=form)

        if short_name == '' or short_name is None:
            short_name = get_unique_short_id()

        url_map = URL_map(
            original=form.original_link.data,
            short=short_name,
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template(
            'yacut.html',
            form=form,
            short=short_name
        ), HTTPStatus.OK
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    '''Редирект на новую ссылку.'''
    url_map = URL_map.query.filter_by(short=short).first()
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    original_url = url_map.original
    return redirect(original_url)
