from main import chatbotdb
from flask import Flask, request, jsonify
from main import chatbotdb
app = Flask(__name__)

@app.route('/question', methods=['GET','POST'])
def chat():
    return jsonify({'question': "Sony?"})

if __name__ == '__main__':
    app.run(port=5001)
