from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import app, db, photos
from .models import Brand, Product
from .forms import Products
import secrets
import os


def brands():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return brands


@app.route('/')
def home():
    products = Product.query.filter(Product.stock > 0)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return render_template('customer/home_customer.html', products=products, brands=brands)


@app.route('/brand/<int:id>')
def get_brand(id):
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand_id=id)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return render_template('customer/home_customer.html', brand=brand, brands=brands, get_brand=get_brand)


@app.route('/product/<int:id>')
def detail_page(id):
    product = Product.query.get_or_404(id)
    return render_template('customer/detail.html', product=product, brands=brands())


@app.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Pomyślnie dodano producenta', 'success')
        db.session.commit()
        return redirect(url_for('add_brand'))
    return render_template('products/add_brand.html', title='Dodaj producenta', brands='brands')


@app.route('/update_brand/<int:id>', methods=['GET', 'POST'])
def update_brand(id):
    if 'email' not in session:
        flash('Najpierw się zaloguj', 'danger')
        return redirect(url_for('login'))
    update_brand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        update_brand.name = brand
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/add_brand.html', title='Udate brand', brands='brands', update_brand=update_brand)


@app.route('/delete_brand/<int:id>', methods=['GET', 'POST'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        flash(f"Usunięto producenta", "success")
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f"Błąd przy usuwaniu producenta", "warning")
    return redirect(url_for('admin'))


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = Products(request.form)
    brands = Brand.query.all()
    if request.method == "POST" and 'image' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        brand = request.form.get('brand')
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        add_product = Product(name=name, price=price, discount=discount, stock=stock, desc=desc,
                              brand_id=brand, image=image)
        db.session.add(add_product)
        flash(f'Produkt dodany', 'success')
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('products/add_product.html', form=form, title='Prześlij', brands=brands)


@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    form = Products(request.form)
    product = Product.query.get_or_404(id)
    brands = Brand.query.all()
    brand = request.form.get('brand')
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.description.data
        product.brand_id = brand
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image))
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
            except:
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        flash('Zaktualizowano', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc
    return render_template('products/add_product.html', form=form, title='Zaaktualizuj produkt', getproduct=product,
                           brands=brands)


@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'Usunięto produkt', 'success')
        return redirect(url_for('product'))
    flash(f'Błąd przy usuwaniu', 'success')
    return redirect(url_for('admin'))