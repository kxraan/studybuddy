from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, URL, Optional
from wtforms.fields import DateTimeLocalField
from flask_wtf.file import FileField, FileAllowed



class CreateGroupForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    tags = StringField('Tags (comma-separated)', validators=[Length(max=200)])
    submit = SubmitField('Create Group')

class ScheduleSessionForm(FlaskForm):
    date_time = DateTimeLocalField(
        'Session Date & Time',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )
    zoom_link = StringField('Zoom Link (optional)', validators=[Optional(), URL()])
    submit = SubmitField('Schedule Session')




class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=300)])
    file = FileField('Upload File (PDF, PNG, JPG only)', validators=[
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'Only PDF, PNG, JPG files are allowed.')
    ])
    link = StringField('External Link (optional)', validators=[Optional(), URL()])
    submit = SubmitField('Upload Resource')


class CommentForm(FlaskForm):
    content = TextAreaField('Leave a comment', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Post Comment')

