from flask import Flask, request, jsonify, render_template
from model import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hack',methods=['POST'])
def hack():
    username = [str(x) for x in request.form.values()]
    username = username[0]

    output = findEmailFromUsername(username)

    return render_template('index.html', user=f'Username: {username}',email=f"Email: {output.split(':')[1]}")


if __name__ == "__main__":
    app.run(debug=True)