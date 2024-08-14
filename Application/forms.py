from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductForm(FlaskForm):
    # Field for the product name
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(max=100, message='Name must be less than 100 characters')
        ]
    )
    
    # Field for the product price
    price = DecimalField(
        'Price',
        places=2,
        validators=[
            DataRequired(message='Price is required'),
            NumberRange(min=0.01, message='Price must be a positive number')
        ]
    )
    
    # Field for the product category
    category = SelectField(
        'Category',
        choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('books', 'Books'), ('home', 'Home')],
        validators=[DataRequired(message='Category is required')]
    )
    
    # Field for the product rating
    rating = IntegerField(
        'Rating',
        validators=[
            Optional(),
            NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
        ]
    )
    
    # Field for the product description
    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=500, message='Description must be less than 500 characters')]
    )
    
    # Field for the product company
    company = StringField(
        'Company',
        validators=[Optional(), Length(max=100, message='Company name must be less than 100 characters')]
    )
