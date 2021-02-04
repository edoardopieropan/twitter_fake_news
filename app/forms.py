from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class TweetsSetDownloadForm(FlaskForm):
    set_name = StringField("Set Name", validators=[DataRequired()])
    search_query = StringField("Search Query", validators=[DataRequired()])
    tweets_number = SelectField("Number of tweets", validators=[DataRequired()],
                                choices=[str(i) for i in range(1, 21)])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    tweets_set_to_use = SelectField("Tweets Set", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FieldsRequiredForm(FlaskForm):
    """Require all fields to have content. This works around the bug that WTForms radio
    fields don't honor the `DataRequired` or `InputRequired` validators.
    """

    class Meta:
        def render_field(self, field, render_kw):
            if field.type == "_Option":
                render_kw.setdefault("required", True)
            return super().render_field(field, render_kw)


class TestForm(FieldsRequiredForm):
    submit = SubmitField("Submit")
