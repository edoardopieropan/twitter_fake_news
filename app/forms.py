from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import html5 as h5fields


class TweetsSetDownloadForm(FlaskForm):
    set_name = StringField("Set Name", validators=[DataRequired()])
    search_query = StringField("Search Query", validators=[DataRequired()])
    tweets_number = SelectField("Number of tweets", validators=[DataRequired()],
                                choices=[str(i) for i in range(1, 21)])
    bufale_pages = SelectField("Fact checking pages", validators=[DataRequired()],
                                choices=[str(i) for i in range(1, 10)])
    submit = SubmitField("Download it")


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # age = StringField("Age", validators=[DataRequired()])
    age = h5fields.IntegerField("Age", validators=[DataRequired()])
    gender = SelectField("Gender", validators=[DataRequired()],
                         choices=["Female", "Male", "Other"])
    tweets_set_to_use = SelectField("Tweet Set", validators=[DataRequired()])
    submit = SubmitField("Start")


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
    submit = SubmitField("Send results")
