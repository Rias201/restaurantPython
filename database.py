import mysql.connector

def connectdb():
    conn = mysql.connector.connect(
        host="localhost",
        database="restaurant",
        user="root",
        password=""
    )
    return conn

def disconnectdb(conn):
    conn.close()

def afegir_comanda(conn,n_comanda,producte,quantitat):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO comandes VALUES (%s,%s,%s)", (n_comanda,producte,quantitat))
        cursor.close()
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        cursor.close()

def recollir_comanda(conn,n_comanda):
    cursor = conn.cursor()
    cursor.execute("SELECT producte, quantitat FROM comandes WHERE id = %s", (n_comanda,))
    json = cursor.fetchall()
    cursor.close()
    return json

def recollir_productes(conn,tipus):
    cursor = conn.cursor()
    cursor.execute("SELECT nom, preu, stock FROM productes WHERE tipus = %s", (tipus,))
    llista_productes = cursor.fetchall()
    cursor.close()
    return llista_productes