from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.route('/api/documents', methods=['GET'])
def get_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents')
    documents = cursor.fetchall()
    conn.close()

    # Convert each row into a dictionary
    documents_list = [dict(document) for document in documents]
    return jsonify(documents_list)

@app.route('/api/documents/<int:id>', methods=['GET'])
def get_document(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents WHERE id = ?', (id,))
    document = cursor.fetchone()
    conn.close()

    if document is None:
        return jsonify({'error': 'Document not found'}), 404

    return jsonify(dict(document))

# if __name__ == '__main__':
#     app.run(debug=True)
