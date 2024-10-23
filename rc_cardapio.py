import mysql.connector


config = {
    'user': 'root',
    'host': 'localhost',
    'port': 3306,
    'database': 'cardapio'
}

def create_produto (prod_name,prod_price,categoria):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO db_cardapio(prod_name, prod_price, categoria) VALUES(%s,%s,%s)",(prod_name,prod_price,categoria))
    connection.commit()
    cursor.close()
    connection.close()
    print("Produto inserido com sucesso.")

def read_produtos(pagina,limite):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    offset = (pagina - 1) * limite
    cursor.execute("SELECT * FROM db_cardapio LIMIT %s OFFSET %s", (limite, offset))
    db_cardapio = cursor.fetchall()
    cursor.close()
    connection.close()
    return db_cardapio

def update_produto(id, prod_name,prod_price,categoria):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("UPDATE db_cardapio SET prod_name = %s, prod_price = %s, categoria = %s WHERE id = %s", (prod_name, prod_price, categoria,id))
    connection.commit()
    cursor.close()
    connection.close()
    print("Produto atualizado com sucesso.")

def delete_produto(id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM db_cardapio WHERE id = %s", (id))
    connection.commit
    connection.close
    print("Produto deletado com sucesso.")

if __name__ == "__main__":
    create_produto("X-Bacon",12.99,"Tradicionais")

    read_produtos(1,5)