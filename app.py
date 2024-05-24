#importando o FLASK

from flask import Flask, request, jsonify
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
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Produt added successfully"})
    return jsonify({"message": "Invalid product data"}), 400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    
    # RECUPERAR O PRODUTO DA BASE DE DADOS
    # VERIFICAR SE O PRODUTO É VÁLIDO
    # SE EXISTE, APAGAR DA BASE DE DADOS
    # SE NÃO EXISTE, RETORNAR NOT FOUND
    
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produt delete successfully"})
    return jsonify({"message": "Product not found"}), 404
        
#definir um rota raiz (Pagina inicial) e a função que sera executada ao requisitar
@app.route('/teste')
def hello_word():
    return 'Hello Word'

if __name__ == "__main__":
    app.run(debug=True)
