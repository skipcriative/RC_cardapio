from flask import Flask, request, jsonify
import mysql.connector

config = {
    'database': 'skipcr49_rc_cardapio',
    'user': 'skipcr49_junior',
    'password': 'Junior@Skip#24',
    'host': '192.185.211.8',
    'port': '3306'
}

app = Flask(__name__)

@app.route('/')
def home():
    return "hello"

#create new product
@app.route('/products',methods=['POST'])
def create_produto ():

    data = request.get_json()           #request reads the context of the http request
    prod_name = data.get('prod_name')
    prod_price = data.get('prod_price')
    categoria = data.get('categoria')

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO rc_cardapio(prod_name, prod_price, categoria) VALUES(%s,%s,%s)",(prod_name,prod_price,categoria))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"messege": "Produto inserido"}), 201


#read all products paginated 
@app.route('/products',methods=['GET'])
def read_produtos():

    pagina = int (request.args.get('pagina',1))
    limite = int (request.args.get('limite',10))

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    offset = (pagina - 1) * limite
    cursor.execute("SELECT * FROM rc_cardapio LIMIT %s OFFSET %s", (limite, offset))
    rc_cardapio = cursor.fetchall()
    cursor.close()
    connection.close()
    return rc_cardapio



#updates a product
@app.route('/products/<int:id>', methods=['PUT'])
def update_produto(id):

    data = request.get_json()           #request reads the context of the http request
    prod_name = data.get('prod_name')
    prod_price = data.get('prod_price')
    categoria = data.get('categoria')


    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("UPDATE rc_cardapio SET prod_name = %s, prod_price = %s, categoria = %s WHERE id = %s", (prod_name, prod_price, categoria,id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"messege": "Produto alterado"}), 200



@app.route('/products/<int:id>', methods=['DELETE'])
def delete_produto(id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM rc_cardapio WHERE id = %s", (id,))
    connection.commit()
    connection.close()
    
    return jsonify({"messege": "Produto deletado"}), 204



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
