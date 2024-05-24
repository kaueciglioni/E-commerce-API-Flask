#importando o FLASK

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

#Modelagem
#Produto (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
     
@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    return data

#definir um rota raiz (Pagina inicial) e a função que sera executada ao requisitar

@app.route('/teste')
def hello_word():
    return 'Hello Word'

if __name__ == "__main__":
    app.run(debug=True)
