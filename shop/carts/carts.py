from shop import app
from flask import render_template, session, request, redirect, url_for, flash
from shop.products.routes import brands
from shop.products.models import Product


def merge(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/add_cart', methods=['POST'])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Product.query.filter_by(id=product_id).first()

        if request.method == "POST":
            dict_items = {
                product_id: {'name': product.name, 'price': float(product.price), 'discount': product.discount,
                             'quantity': quantity, 'image': product.image}}
            if 'shopping_cart' in session:
                print(session['shopping_cart'])
                if product_id in session['shopping_cart']:
                    for key, item in session['shopping_cart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['shopping_cart'] = merge(session['shopping_cart'], dict_items)
                    return redirect(request.referrer)
            else:
                session['shopping_cart'] = dict_items
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def get_cart():
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    for key, product in session['shopping_cart'].items():
        discount = (product['discount'] / 100) * float(product['price']) * float(product['quantity'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        subtotal = float("%.2f" % subtotal)
    return render_template('customer/carts.html', brands=brands(), subtotal=subtotal)


@app.route('/update_cart/<int:code>', methods=['POST'])
def update_cart(code):
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['shopping_cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Zaktualizowano')
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))


@app.route('/delete_item/<int:id>')
def delete_item(id):
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['shopping_cart'].items():
            if int(key) == id:
                session['shopping_cart'].pop(key, None)
                return redirect(url_for('get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('get_cart'))


@app.route('/clear_cart')
def clear_cart():
    try:
        session.pop('shopping_cart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)