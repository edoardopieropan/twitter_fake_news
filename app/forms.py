from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class TweetsSetDownloadForm(FlaskForm):
    set_name = StringField("Set Name", validators=[DataRequired()])
    search_keyword = StringField("Search Keyword", validators=[DataRequired()])
    tweets_number = SelectField("Number of tweets", validators=[DataRequired()],
                                choices=[str(i) for i in range(1, 21)])
    submit = SubmitField("Submit")
