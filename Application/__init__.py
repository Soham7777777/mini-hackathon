from flask import Flask, flash, redirect, render_template, url_for
from instance import IApplicationConfiguration
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(MappedAsDataclass, DeclarativeBase):
    pass

db: SQLAlchemy = SQLAlchemy(model_class=Base)

def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    # import Application.error_handlers as errhndl
    # app.register_error_handler(exceptions.HTTPException, errhndl.jsonify_default_errors)
    # app.register_error_handler(exceptions.NotFound, errhndl.handle_notfound_errors)
    
    db.init_app(app)
    from Application.models import Product
    with app.app_context():
        db.create_all()

    from Application.forms import ProductForm
    @app.route('/', methods=['GET', 'POST'])
    def home():
        form = ProductForm()
        if form.validate_on_submit():
            new_product = Product(
                name=form.name.data,
                price=form.price.data,
                category=form.category.data,
                rating=form.rating.data,
                description=form.description.data,
                company=form.company.data
            )
            db.session.add(new_product)
            db.session.commit()

            flash('Product added successfully!', 'success')
            return redirect(url_for('show_products'))

        return render_template('form.html', form=form)
        
    
    @app.route('/products')
    def show_products():
        products = Product.query.all()  # Query all products from the database
        return render_template('index.html', products=products)


    return app