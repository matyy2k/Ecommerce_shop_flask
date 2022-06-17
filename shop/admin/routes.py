from flask import render_template, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import Admin
from shop.products.models import Product, Brand
from shop.customers.models import Customer
from flask_login import login_user, login_required
from shop.customers.forms import CustomerRegisterForm





@app.route('/admin')
def admin():
    return render_template('admin/home_admin.html')

@app.route('/moderator')
def moderator():
    return render_template('moderator/home_moderator.html')


@app.route('/products')
def product():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)


@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands', brands=brands)


@app.route('/users')
def users():
    admins = Admin.query.all()
    customers = Customer.query.all()
    return render_template('admin/users.html', admins=admins, customers=customers)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = RegistrationForm()
    if request.method == "POST":
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = Admin(username=form.username.data, email=form.email.data,
                     password=hash_password, admin=form.admin.data, moderator=form.moderator.data)
        db.session.add(user)
        flash(f'welcome {form.username.data} Thanks for registering', 'success')
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('admin/add_admin_moderator.html', form=form, title='Dodaj użytkownika')


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = RegistrationForm(request.form)
    user = Admin.query.get_or_404(id)
    if request.method == "POST":
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        flash('The product was updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.username.data = user.username
    form.email.data = user.email
    form.password.data = user.password
    return render_template('admin/add_admin_moderator.html', form=form, user=user, title='Zaaktualizuj użytkownika')


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    admins = Admin.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(admins)
        flash(f"The brand {admins.username} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('users'))
    flash(f"The brand {admins.username} can't be  deleted from your database", "warning")
    return render_template('admin/users.html', admins=admins)


@app.route('/update_cust/<int:id>', methods=['GET', 'POST'])
def update_cust(id):
    form = CustomerRegisterForm(request.form)
    user = Customer.query.get_or_404(id)
    if request.method == "POST":
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.country = form.country.data
        user.city = form.city.data
        user.contact = form.contact.data
        user.address = form.address.data
        user.zipcode = form.zipcode.data
        flash('The product was updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.username.data = user.username
    form.password.data = user.password
    form.email.data = user.email
    form.city.data = user.city
    form.contact.data = user.contact
    form.address.data = user.address
    form.zipcode.data = user.zipcode
    return render_template('admin/add_customer.html', form=form, user=user, title='Zaaktualizuj użytkownika')


@app.route('/delete_cust/<int:id>', methods=['GET', 'POST'])
def delete_cust(id):
    customer = Admin.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(customer)
        flash(f"The brand {customer.username} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('users'))
    flash(f"The brand {customer.username} can't be  deleted from your database", "warning")
    return render_template('admin/users.html', customer=customer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Admin(username=form.username.data, email=form.email.data,
                            password=hash_password)
        db.session.add(register)
        flash(f'Welcome {form.username.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            return redirect(url_for('admin'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/login.html', form=form)