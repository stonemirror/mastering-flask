from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    BooleanField
)
from wtforms.validators import DataRequired, Length, EqualTo, URL
from webapp.models import User


#
# Forms
#
class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(
        u'Comment',
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(max=255)]
    )
    Password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        #
        # Did we fail a validation test?
        #
        if not check_validate:
            return False
        user = User.query.filter_by(
            username=self.username.data
        ).first()
        #
        # Does the username exist?
        #
        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False
        #
        # Do the password hashes match?
        #
        if not self.user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )
            return False
        #
        # Looks good, let 'em through...
        #
        return True


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(max=255)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )
    confirm = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo(password)]
    )
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(
            username=self.username.data
        ).first()
        if user:
            self.username.errors.append(
                'A user with that name already exists'
            )
            return False
        return True


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(
        'Content',
        validators=[DataRequired()]
    )
