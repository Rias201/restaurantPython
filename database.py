import mysql.connector, datetime

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
        # print(e)
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
        # print(e)
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
        # print(e)
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
    llista = cursor.fetchall()
    cursor.close()
    disconnectdb(conn)
    return llista

def recollir_productes(tipus):
    conn = connectdb()
    cursor = conn.cursor()
    cursor.execute("SELECT nom, preu, stock, imatge FROM productes WHERE tipus = %s", (tipus,))
    llista_productes = cursor.fetchall()
    cursor.close()
    disconnectdb(conn)
    return llista_productes

def historic(data):
    conn = connectdb()
    cursor = conn.cursor()
    cursor.execute("SELECT r.id, r.id_taula, c.producte, c.quantitat FROM registres r LEFT JOIN comandes c ON r.id = c.id WHERE r.data = %s", (data,))
    dicc = dict()
    for i in cursor.fetchall():
        # print(i)
        if i[0] not in dicc:
            dicc[i[0]] = [i[1],[]]
        dicc[i[0]][1].append([i[2], i[3]])
    cursor.close()
    disconnectdb(conn)
    return dicc