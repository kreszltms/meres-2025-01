from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'nevnapok'
}

def query_database(sql, params=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, params)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/api/nevnapok/', methods=['GET'])
def nevnapok():
    nap = request.args.get('nap')
    nev = request.args.get('nev')

    if nap:
        sql = "SELECT * FROM nevnapok WHERE datum = %s"
        results = query_database(sql, (nap,))
        if results:
            return jsonify({"datum": results[0]['datum'], "nevnap1": results[0]['nevnap1'], "nevnap2": results[0].get('nevnap2', None)})
        else:
            return jsonify({"hiba": "nincs találat"}), 404

    elif nev:
        sql = "SELECT * FROM nevnapok WHERE nevnap1 = %s OR nevnap2 = %s LIMIT 1"
        results = query_database(sql, (nev, nev))
        if results:
            return jsonify({"datum": results[0]['datum'], "nevnap1": results[0]['nevnap1'], "nevnap2": results[0].get('nevnap2', None)})
        else:
            return jsonify({"hiba": "nincs találat"}), 404

    else:
        return jsonify({"minta1": "/?nap=12-31", "minta2": "/?nev=Szilveszter"}), 400

if __name__ == '__main__':
    app.run(debug=True)
