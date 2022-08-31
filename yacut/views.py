from http.client import NOT_FOUND, OK
from flask import redirect, render_template
from http import HTTPStatus

from . import app, db
from .forms import URLForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data or get_unique_short_id()
    url_map = URL_map(
        original=form.original_link.data,
        short=short
    )
    db.session.add(url_map)
    db.session.commit()
    return render_template('index.html', form=form, short=short), HTTPStatus.OK


@app.route('/<string:short>')
def short_view(short):
    return redirect(
        URL_map.query.filter_by(short=short).first_or_404().original)
