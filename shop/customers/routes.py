from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from shop import app, db, bcrypt
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Customer, CustomerOrder


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
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
        return redirect(url_for('profile', id=current_user.id))
    form.username.data = user.username
    form.email.data = user.email
    form.city.data = user.city
    form.contact.data = user.contact
    form.address.data = user.address
    form.zipcode.data = user.zipcode
    return render_template('customer/profile.html', form=form, user=user, title='Zaaktualizuj użytkownika')


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Customer(username=form.username.data, email=form.email.data,
                            password=hash_password, country=form.country.data, city=form.city.data,
                            contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Użytkownik {form.username.data} zarejestrowany.', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_type'] = 'customer'
            login_user(user)
            flash('Jesteś zalogowany!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Niepoprawny login albo hasło', 'danger')
        return redirect(url_for('customer_login'))
    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
    return updateshoppingcart


@app.route('/order')
def order():
    if current_user.is_authenticated:
        name = CustomerOrder(name=session['Shoppingcart']['1']['name'])
        db.session.add(name)
        db.session.commit()
        flash('Zamówienie udane', 'success')
        return redirect(url_for('orders'))


@app.route('/orders')
def orders():
    form = CustomerOrder()
    orders = CustomerOrder.query.all()
    return render_template('customer/orders.html', form=form, orders=orders)