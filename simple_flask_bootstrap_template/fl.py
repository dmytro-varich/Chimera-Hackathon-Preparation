from flask import Flask, render_template, redirect, flash, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, NumberRange
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key_lol'


# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Key SQLAlchemy Data Types
# db.Integer: For integers.
# db.String(size): For variable-length strings, with a maximum size specified.
# db.Text: For longer text fields.
# db.Float: For floating-point (approximate real) numbers.
# db.Numeric(precision, scale): For fixed-point decimal numbers (e.g., Numeric(10, 2) for a total of 10 digits, 2 of which are after the decimal).
# db.Boolean: For true/false values.
# db.Date: For storing dates (YYYY-MM-DD).
# db.DateTime: For storing date and time (YYYY-MM-DD HH:MM
# ).
# db.Time: For storing time only (HH:MM
# ).
# db.Enum: For enumerated types, specifying a fixed set of valid values.
# db.JSON: For JSON objects.
# db.LargeBinary: For binary data, such as files.

# Database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    percent = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

# Initialize the database
def create_tables():
    with app.app_context():
        db.create_all()


# Possible form fields
# name = StringField('Name', validators=[DataRequired()])
# email = StringField('Email', validators=[DataRequired(), Email()])
# description = TextAreaField('Description')
# password = PasswordField('Password', validators=[DataRequired()])
# age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
# height = FloatField('Height', validators=[DataRequired(), NumberRange(min=0.0)])
# price = DecimalField('Price', validators=[DataRequired()])
# is_active = BooleanField('Active')
# gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
# country = SelectField('Country', choices=[('us', 'USA'), ('ca', 'Canada')])
# languages = SelectMultipleField('Languages', choices=[('py', 'Python'), ('js', 'JavaScript')])
# upload = FileField('Upload File')
# birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])
# appointment = DateTimeField('Appointment Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
# csrf_token = HiddenField()
# submit = SubmitField('Submit')

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    percent = FloatField('Float', validators=[DataRequired()])
    quantity = IntegerField('Integer', validators=[DataRequired(), NumberRange(min=0)])  # Integer Field
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/items', methods=['GET'])
def get_items():
    # Retrieve all items from the database
    items = Item.query.all()  # This fetches all rows from the 'Item' table

    # Pass the items to the template
    return render_template('get_items.html', items=items)

@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        percent = form.percent.data
        quantity = form.quantity.data

        # Check if the user with this email already exists
        existing_user = Item.query.filter_by(name=name).first()
        if existing_user:
            flash('This name is already registered', 'danger')
        else:
            # If the user does not exist, add them to the database
            new_item = Item(name=name, percent=percent, quantity=quantity)
            db.session.add(new_item)
            db.session.commit()

            # flash(f'Product, {name}, {percent}, {quantity} added', 'success')

            # Clear the form (optional, you can re-render with empty data)
            form.name.data = ''
            form.percent.data = ''
            form.quantity.data = ''

            return redirect(url_for('get_items'))

    return render_template('create_item.html', form=form)


@app.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = MyForm()

    if form.validate_on_submit():
        # Update the item's attributes
        item.name = form.name.data
        item.percent = form.percent.data
        item.quantity = form.quantity.data

        try:
            db.session.commit()
            flash(f"Item '{item.name}' has been updated!", "success")
            return redirect(url_for('get_items'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while trying to update the item.", "danger")

    # Pre-fill form fields with current item data
    form.name.data = item.name
    form.percent.data = item.percent
    form.quantity.data = item.quantity

    return render_template('update_item.html', form=form, item=item)


@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # Query the item by ID
    item_to_delete = Item.query.get_or_404(item_id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f"Item '{item_to_delete.name}' has been deleted!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while trying to delete the item.", "danger")

    return redirect(url_for('get_items'))


# # LLM routing
# @app.route("/llm")
# def llm_page():
#     return "<a href='http://localhost:8501' target='_blank'>Open LLM Interaction</a>"


@app.route('/process_llm', methods=['POST'])
def process_query():
    # Get the user input from the POST request
    user_input = request.json.get('query')

    # Process the input (replace this with your actual logic)
    response = f"Processed query: {user_input}"

    # Return the processed response
    return jsonify({"response": response})



if __name__ == '__main__':
    # Ensure tables are created before running the app
    create_tables()
    app.run(debug=True)
