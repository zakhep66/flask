from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

from cloudipsp import Api, Checkout

app = Flask(__name__)
# выбираем СУБД, сейчас стоит 'sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.title


@app.route('/')
def home():
    items = Item.query.order_by(Item.price).all()
    # if items == []:
    #     return render_template('index.html') + "В базе пусто"
    return render_template('index.html', items=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>/del')
def boughtDel(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return 'Что-то пошло не по плану'


@app.route('/buy/<int:id>')
def bought(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1397120,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return url


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except:
            return 'Что-то пошло не по плану'
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
