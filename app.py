from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import math
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/evaluate', methods=['GET'])
def evaluate():
    operation = request.args.get('op')
    value = request.args.get('value')
    mode = request.args.get('mode', 'degree')

    try:
        value = float(value)
    except:
        return jsonify({"error": "Invalid number input"}), 400

    if mode == 'degree':
        value = math.radians(value)

    if operation == 'sin':
        result = math.sin(value)
    elif operation == 'cos':
        result = math.cos(value)
    elif operation == 'tan':
        result = math.tan(value)
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({
        "operation": operation,
        "mode": mode,
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
