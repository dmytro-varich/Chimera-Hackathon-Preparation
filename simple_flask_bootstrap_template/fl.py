from flask import Flask, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key_lol'


# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Initialize the database
def create_tables():
    with app.app_context():
        db.create_all()

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        # Check if the user with this email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered!', 'danger')
        else:
            # If the user does not exist, add them to the database
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()

            flash(f'Hello, {name}, {email}!', 'success')

            # Clear the form (optional, you can re-render with empty data)
            form.name.data = ''
            form.email.data = ''

    return render_template('main.html', form=form)


if __name__ == '__main__':
    # Ensure tables are created before running the app
    create_tables()
    app.run(debug=True)
