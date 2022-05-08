# yacut/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class URL_map_Form(FlaskForm):
    """
    original_link — поле для оригинальной длинной ссылки,
    custom_id — поле для пользовательского варианта
    короткого идентификатора.
    """
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 6),
            Optional(),
        ]
    )
    submit = SubmitField('Добавить')
