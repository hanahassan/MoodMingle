from flask import Flask, jsonify, request

app = Flask(__name__)

# http://127.0.0.1:5000/api/data - run on this web address and you should see message
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Flask!'})

if __name__ == '__main__':
    app.run(debug=True)
