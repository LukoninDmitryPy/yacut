from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional,
                                Regexp, ValidationError)

from .models import URL_map


class URLForm(FlaskForm):
    original_link = URLField(
        'Ссылка для сокращения',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Вариант сокращения', validators=[
            Length(1, 16), Optional(), Regexp(
                r'^[A-Za-z0-9]+$',
                message='Можно использовать только [A-Za-z0-9]')])
    submit = SubmitField('Сократить')

    def validate_custom_id(self, field):
        if field.data and URL_map.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!')
