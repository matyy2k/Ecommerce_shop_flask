from flask import render_template, request, redirect, url_for, flash, session
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import Admin
from shop.products.models import Product, Brand
from shop.customers.models import Customer
from flask_login import login_user, login_required, current_user
from shop.customers.forms import CustomerRegisterForm


@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        try:
            if current_user.country:
                return redirect('login')
        except:
            return render_template('admin/home_admin.html')


@app.route('/moderator')
@login_required
def moderator():
    if current_user.is_authenticated:
        try:
            if current_user.country:
                return redirect('login')
        except:
            return render_template('moderator/home_moderator.html')


@app.route('/products')
@login_required
def product():
    if current_user.is_authenticated:
        try:
            if current_user.country:
                return redirect('login')
        except:
            products = Product.query.all()
            return render_template('admin/products.html', products=products)


@app.route('/brands')
@login_required
def brands():
    if current_user.is_authenticated:
        try:
            if current_user.country:
                return redirect('login')
        except:
            brands = Brand.query.order_by(Brand.id.desc()).all()
            return render_template('admin/brand.html', title='brands', brands=brands)


@app.route('/users')
@login_required
def users():
    if current_user.is_authenticated:
        try:
            if current_user.country or current_user.moderator:
                return redirect('login')
        except:
            admins = Admin.query.all()
            customers = Customer.query.all()
            return render_template('admin/users.html', admins=admins, customers=customers)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.is_authenticated or current_user.moderator:
        try:
            if current_user.country:
                return redirect('login')
        except:
            form = RegistrationForm()
            if request.method == "POST":
                hash_password = bcrypt.generate_password_hash(form.password.data)
                user = Admin(username=form.username.data, email=form.email.data,
                             password=hash_password, admin=form.admin.data, moderator=form.moderator.data)
                db.session.add(user)
                flash(f'Rejestracja udana', 'success')
                db.session.commit()
                return redirect(url_for('users'))
            return render_template('admin/add_admin_moderator.html', form=form, title='Dodaj użytkownika')


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = RegistrationForm(request.form)
    user = Admin.query.get_or_404(id)
    if request.method == "POST":
        user.username = form.username.data
        user.email = form.email.data
        user.admin = form.admin.data
        user.moderator = form.moderator.data
        flash('Aktualizacja użytkownika udana', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.username.data = user.username
    form.email.data = user.email
    form.admin.data = user.admin
    form.moderator.data = user.moderator
    return render_template('admin/update_user.html', form=form, user=user, title='Zaaktualizuj użytkownika')


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if current_user.is_authenticated or current_user.moderator:
        try:
            if current_user.country:
                return redirect('login')
        except:
            admins = Admin.query.get_or_404(id)
            if request.method == "POST":
                db.session.delete(admins)
                flash(f"Użytkownik usunięty", "success")
                db.session.commit()
                return redirect(url_for('users'))
            flash(f"Problem z usunięciem", "warning")
            return render_template('admin/users.html', admins=admins)


@app.route('/update_cust/<int:id>', methods=['GET', 'POST'])
@login_required
def update_cust(id):
    form = CustomerRegisterForm(request.form)
    user = Customer.query.get_or_404(id)
    if request.method == "POST":
        user.username = form.username.data
        user.email = form.email.data
        user.country = form.country.data
        user.city = form.city.data
        user.contact = form.contact.data
        user.address = form.address.data
        user.zipcode = form.zipcode.data
        flash('Aktualizacja użytkownika udana', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.username.data = user.username
    form.email.data = user.email
    form.city.data = user.city
    form.contact.data = user.contact
    form.address.data = user.address
    form.zipcode.data = user.zipcode
    return render_template('admin/add_customer.html', form=form, user=user, title='Zaaktualizuj użytkownika')


@app.route('/delete_cust/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_cust(id):
    if current_user.is_authenticated:
        try:
            if current_user.country:
                return redirect('login')
        except:
            customer = Customer.query.get_or_404(id)
            if request.method == "POST":
                db.session.delete(customer)
                flash(f"Użytkownik usunięty", "success")
                db.session.commit()
                return redirect(url_for('users'))
            flash(f"Problem z usunięciem", "warning")
            return render_template('admin/users.html', customer=customer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = Admin(username=form.username.data, email=form.email.data,
                     password=hash_password, admin=form.admin.data, moderator=form.moderator.data)
        db.session.add(user)
        flash(f'Użytkownik {form.username.data} zarejestrowany.', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/register.html', title='Register user', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_type'] = 'admin'
            login_user(user)
            flash('Jesteś zalogowany', 'success')
            if user.admin == '1':
                return redirect(url_for('admin'))
            elif user.admin == '0':
                return redirect(url_for('moderator'))
        flash('Niepoprawny login albo hasło', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/login.html', form=form)