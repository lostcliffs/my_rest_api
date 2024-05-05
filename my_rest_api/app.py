from flask import Flask, jsonify, request
import pymssql

app = Flask(__name__)

def create_resource_to_database(ADSOYAD, SEHIR, BOLUM):
    try:
        conn = pymssql.connect(server='server_name', user='username', password='password', database='database_name')
        cursor = conn.cursor()
        sql_query = "INSERT INTO BILGILER (ADSOYAD, SEHIR, BOLUM) VALUES ( %s, %s, %s)"
        values = (ADSOYAD, SEHIR, BOLUM)
        cursor.execute(sql_query, values)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Veritabanında belirli kaynağı güncelleme hatası:", e)
        return None

def get_all_resources_from_database():
    try:
        conn = pymssql.connect(server='DESKTOP-2PIN5K3/SQLEXPRESS', user='DESKTOP-2PIN5K3/MYCOM', password='1234', database='OGRENCILER')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BILGILER')
        resources = cursor.fetchall()
        conn.close()
        return resources
    except Exception as e:
        print("Veritabanından kaynakları alma hatası:", e)
        return None

def get_resource_from_database(resource_id):
    try:
        conn = pymssql.connect(server='DESKTOP-2PIN5K3/SQLEXPRESS', user='DESKTOP-2PIN5K3/USER', password='1234', database='OGRENCILER')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BILGILER WHERE ID = '+resource_id)
    except Exception as e:
        print("Veritabanından belirli kaynağı alma hatası:", e)
        return None

def update_resource_to_database(resource_id, ADSOYAD, SEHIR, BOLUM):
    try:
        conn = pymssql.connect(server='server_name', user='username', password='password', database='database_name')
        cursor = conn.cursor()
        sql_query = "UPDATE BILGILER SET (ADSOYAD = %s, SEHIR = %s, BOLUM = %s) WHERE ID = %s"
        values = (ADSOYAD, SEHIR, BOLUM, resource_id)
        cursor.execute(sql_query, values)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Veritabanında belirli kaynağı güncelleme hatası:", e)
        return None

def delete_resource_from_database(resource_id):
    try:
        conn = pymssql.connect(server='DESKTOP-2PIN5K3/SQLEXPRESS', user='DESKTOP-2PIN5K3/USER', password='1234', database='OGRENCILER')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BILGILER WHERE ID = '+resource_id)
    except Exception as e:
        print("Veritabanından belirli kaynağı silme hatası:", e)
        return None

# Create, Read, Update, Delete, List metotları
@app.route('/api/resource', methods=['POST'])
def Create():
    data = request.json  # İstekten gelen JSON verisini al
    create_resource_to_database(data['ADSOYAD'], data['SEHIR'], data['BOLUM'])
    return jsonify({'message': 'Resource created successfully'}), 201

@app.route('/api/resource/<resource_id>', methods=['GET'])
def Read(resource_id):
    resource = get_resource_from_database(resource_id) # Belirli bir kaydı veritabanından bulma işlemi
    return jsonify(resource), 200

@app.route('/api/resource/<resource_id>', methods=['PUT'])
def Update(resource_id):
    data = request.json  # İstekten gelen JSON verisini al
    update_resource_to_database(resource_id, data['ADSOYAD'], data['SEHIR'], data['BOLUM'])
    # Belirli bir kaydı güncelleme işlemi
    return jsonify({'message': 'Resource updated successfully'}), 200

@app.route('/api/resource/<resource_id>', methods=['DELETE'])
def Delete(resource_id):
    delete_resource_from_database(resource_id) # Belirli bir kaydı silme işlemi
    return jsonify({'message': 'Resource deleted successfully'}), 200

@app.route('/api/resources', methods=['GET'])
def List():
    resources = get_all_resources_from_database()  # Tüm kaynakları almak için örnek bir işlev
    return jsonify(resources), 200
