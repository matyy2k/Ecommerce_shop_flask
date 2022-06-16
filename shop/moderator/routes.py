from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import LoginForm
from shop.products.models import Product, Brand


@app.route('/moderator')
def moderator():
    products = Product.query.all()
    return render_template('moderator/home_moderator.html', products=products)