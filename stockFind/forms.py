from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
    IntegerRangeField,
    BooleanField
)

from wtforms.validators import (
    InputRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=4,
                max=20,
                message="Your password must be between 4 and 20 characters long.",
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password",
                message="This password did not match the one in the password field.",
            ),
        ],
    )

    submit = SubmitField("Register")


class StockForm(FlaskForm):
    ticker = StringField("Ticker", validators=[InputRequired()])
    company = StringField("Company", validators=[InputRequired()])
    amtInvested = IntegerField("Amount Invested: $ ", validators=[InputRequired()])
    bought = BooleanField("Bought(Y/N)")

    submit = SubmitField("Add Stock")


class StringListField(TextAreaField):
    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        # checks valuelist contains at least 1 element, and the first element isn't falsy (i.e. empty string)
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []


class ExtendedStockForm(StockForm):
    amtInvested = IntegerRangeField("Amount Invested")

    submit = SubmitField("Submit")
