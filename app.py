from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import math
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store calculation history
history = []

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

    # Convert degrees to radians only for trig
    if mode == 'degree' and operation in ["sin", "cos", "tan"]:
        value = math.radians(value)

    # Operations
    if operation == "sin":
        result = math.sin(value)

    elif operation == "cos":
        result = math.cos(value)

    elif operation == "tan":
        result = math.tan(value)

    elif operation == "sqrt":
        result = math.sqrt(value)

    elif operation == "log":
        result = math.log(value)

    else:
        return jsonify({"error": "Invalid operation"}), 400

    # Round result for clean output
    result = round(result, 6)

    # Save history
    history.append({
        "operation": operation,
        "value": request.args.get('value'),
        "mode": mode,
        "result": result,
        "time": str(datetime.now())
    })

    # Logging
    with open("logs.txt", "a") as f:
        f.write(f"{operation} {value} {mode} {result} {datetime.now()}\n")

    return jsonify({
        "operation": operation,
        "mode": mode,
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    })


# API Documentation
@app.route('/docs')
def docs():
    return """
    <h2>Cloud Trigonometric API Documentation</h2>

    <h3>Endpoint</h3>
    /api/v1/evaluate

    <h3>Parameters</h3>
    <ul>
    <li>op = sin | cos | tan | sqrt | log</li>
    <li>value = number</li>
    <li>mode = degree | radian</li>
    </ul>

    <h3>Example</h3>
    /api/v1/evaluate?op=sin&value=30&mode=degree
    """


# History API
@app.route('/api/v1/history')
def get_history():
    return jsonify(history)


# Health Check API
@app.route('/health')
def health():
    return jsonify({"status": "service running"})


if __name__ == '__main__':
    app.run(debug=True)