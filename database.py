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

def create_comanda(n_taula):
    conn = connectdb()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO registres (id_taula) VALUES (%s)",(n_taula,))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        disconnectdb(conn)

def afegir_comanda(n_taula,dicc_productes):
    conn = connectdb()
    cursor = conn.cursor()
    # Segons el n_taula podem saber el n_comanda
    cursor.execute("SELECT MAX(id) FROM registres WHERE id_taula = %s", (n_taula,))
    n_comanda = cursor.fetchone()[0]

    cursor.execute("SELECT producte FROM comandes WHERE id = %s", (n_comanda,))
    # Guardem tots els productes en una llista
    llista_productes = list()
    for tupla in cursor.fetchall():
        llista_productes.append(tupla[0])
    
    try:
        # Recorrem el diccionari que arriba
        for i in range(len(list(dicc_productes.keys()))):
            # print(list(dicc_productes.keys())[i])
            if list(dicc_productes.keys())[i] in llista_productes:
                # print("I'm in")
                # Si el producte ja estava a la bd, fem un update
                index = llista_productes.index(list(dicc_productes.keys())[i])
                cursor.execute("UPDATE comandes SET quantitat = %s WHERE producte = %s AND id = %s",(dicc_productes[llista_productes[index]],llista_productes[index], n_comanda))
            else:
                # print("I'm out")
                # Si no hi era, fem un insert
                cursor.execute("INSERT INTO comandes VALUES (%s,%s,%s)",(n_comanda,list(dicc_productes.keys())[i],dicc_productes[list(dicc_productes.keys())[i]]))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        disconnectdb(conn)

def delete_comanda(n_taula):
    conn = connectdb()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM comandes WHERE id = (SELECT MAX(id) FROM registres WHERE id_taula = %s)",(n_taula,))
        cursor.execute("DELETE FROM registres WHERE id = (SELECT MAX(id) FROM registres WHERE id_taula = %s)",(n_taula,))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        disconnectdb(conn)

def recollir_comanda(n_taula,tipus):
    conn = connectdb()
    cursor = conn.cursor()
    if tipus != '*':        
        cursor.execute("SELECT c.id, c.producte, c.quantitat, p.preu FROM comandes c, productes p WHERE c.id = (SELECT MAX(id) FROM registres WHERE id_taula = %s) AND p.nom = c.producte AND p.tipus = %s", (n_taula,tipus))
    else:
        cursor.execute("SELECT c.id, c.producte, c.quantitat, p.preu FROM comandes c, productes p WHERE c.id = (SELECT MAX(id) FROM registres WHERE id_taula = %s) AND p.nom = c.producte", (n_taula,))
    json = cursor.fetchall()
    cursor.close()
    disconnectdb(conn)
    return json

def recollir_productes(tipus):
    conn = connectdb()
    cursor = conn.cursor()
    cursor.execute("SELECT nom, preu, stock, imatge FROM productes WHERE tipus = %s", (tipus,))
    llista_productes = cursor.fetchall()
    cursor.close()
    disconnectdb(conn)
    return llista_productes

# afegir_comanda(1,{'tallat':2,'freixenet':1,'crema catalana':3,'broquetes de vedella amb verdures a la graella':4})