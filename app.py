from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'  # выбираем СУБД, сейчас стоит 'sqlite'
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
    return render_template('index.html', items=items)

@app.route('/api/home')
def apiHome():
    return json(home())

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Что-то пошло не по плану'
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)