#importando o FLASK

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "minhachave123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db= SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#MODELAGEM

## LOGIN ##
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    
#Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    
    
##### AUTENTICAÇÃO  #####
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



###### LOGIN DO USUARIO #####
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get("username")).first()
    
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message":"Logged in successfully"})
        
    return jsonify({"message": "Unauthorized. Invali credentials"})    
    
    
    
### LOGOUT DO USUARIO ####
@app.route('/logout', methods=['POST'])  
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Loggout in successfully"})
    
    
    
    
#### ADICIONAR PRODUTO ####     
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Produt added successfully"})
    return jsonify({"message": "Invalid product data"}), 400





### DELETAR PRODUTO POR ID ###
@login_required
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produt delete successfully"})
    return jsonify({"message": "Product not found"}), 404




####    PROCURAR O PRODUTO POR ID ###
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product_id, 
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Product not found"}), 404




### UPDATE NO PRODUTO ####


@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    data = request.json
    if 'name' in data:
        product.name = data['name']
        
    if 'price' in data:
        product.price = data['price']
        
    if 'description' in data:
        product.description = data['description']
        
    db.session.commit()
    return jsonify({"message": "Produt updated successfully"})
        
        
### VERIFICAR OS PRODUTOS ####
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id, 
            "name": product.name,
            "price": product.price,
            "description": product.description
        }
        product_list.append(product_data)
    return jsonify(product_list)



    
#definir um rota raiz (Pagina inicial) e a função que sera executada ao requisitar
@app.route('/teste')
def hello_word():
    return 'Hello Word'

if __name__ == "__main__":
    app.run(debug=True)
