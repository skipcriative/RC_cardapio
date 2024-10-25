import mysql.connector
config = {
    'database': 'skipcr49_rc_cardapio',
    'user': 'skipcr49_junior',
    'password': 'Junior@Skip#24',
    'host': '192.185.211.8',
    'port': '3306'
}

def create_produto (prod_name,prod_price,categoria):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO rc_cardapio(prod_name, prod_price, categoria) VALUES(%s,%s,%s)",(prod_name,prod_price,categoria))
    connection.commit()
    cursor.close()
    connection.close()
    print("Produto inserido com sucesso.")

def read_produtos(pagina,limite):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    offset = (pagina - 1) * limite
    cursor.execute("SELECT * FROM rc_cardapio LIMIT %s OFFSET %s", (limite, offset))
    rc_cardapio = cursor.fetchall()
    cursor.close()
    connection.close()
    return rc_cardapio

def update_produto(id, prod_name,prod_price,categoria):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("UPDATE rc_cardapio SET prod_name = %s, prod_price = %s, categoria = %s WHERE id = %s", (prod_name, prod_price, categoria,id))
    connection.commit()
    cursor.close()
    connection.close()
    print("Produto atualizado com sucesso.")

def delete_produto(id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM rc_cardapio WHERE id = %s", (id))
    connection.commit()
    connection.close()
    print("Produto deletado com sucesso.")

if __name__ == "__main__":
    create_produto("X-Bacon", 12.90, "Tradicionais")
    produtos = read_produtos(1, 5)
    for produto in produtos:
        print(produto)
