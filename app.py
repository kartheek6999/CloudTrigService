from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import math
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store calculation history
history = []

# -------------------------
# Expression Solver Function
# -------------------------

def solve_expression(expr, mode="degree"):

    expr = expr.replace("^", "**")

    def trig_replace(match, func):
        val = float(match.group(1))
        if mode == "degree":
            val = math.radians(val)
        return str(func(val))

    # Trigonometric replacements
    expr = re.sub(r"sin\((.*?)\)", lambda m: trig_replace(m, math.sin), expr)
    expr = re.sub(r"cos\((.*?)\)", lambda m: trig_replace(m, math.cos), expr)
    expr = re.sub(r"tan\((.*?)\)", lambda m: trig_replace(m, math.tan), expr)

    # Other math functions
    expr = re.sub(r"sqrt\((.*?)\)", lambda m: str(math.sqrt(float(m.group(1)))), expr)
    expr = re.sub(r"log\((.*?)\)", lambda m: str(math.log(float(m.group(1)))), expr)

    return eval(expr)


# -------------------------
# Home Page
# -------------------------

@app.route('/')
def home():
    return render_template('index.html')


# -------------------------
# BASIC TRIG OPERATIONS API
# -------------------------

@app.route('/api/v1/evaluate', methods=['GET'])
def evaluate():

    operation = request.args.get('op')
    value = request.args.get('value')
    mode = request.args.get('mode', 'degree')

    try:
        value = float(value)
    except:
        return jsonify({"error": "Invalid number input"}), 400

    if mode == 'degree' and operation in ["sin", "cos", "tan"]:
        value = math.radians(value)

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

    result = round(result, 6)

    history.append({
        "operation": operation,
        "value": request.args.get('value'),
        "mode": mode,
        "result": result,
        "time": str(datetime.now())
    })

    with open("logs.txt", "a") as f:
        f.write(f"{operation} {value} {mode} {result} {datetime.now()}\n")

    return jsonify({
        "operation": operation,
        "mode": mode,
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    })


# -------------------------
# COMPLEX TRIG EXPRESSION API
# -------------------------

@app.route('/api/v1/expression', methods=['GET'])
def evaluate_expression():

    expr = request.args.get("expr")
    mode = request.args.get("mode", "degree")

    try:
        result = solve_expression(expr, mode)
        result = round(result, 6)

    except:
        return jsonify({"error": "Invalid expression"}), 400

    history.append({
        "operation": "expression",
        "expression": expr,
        "mode": mode,
        "result": result,
        "time": str(datetime.now())
    })

    with open("logs.txt", "a") as f:
        f.write(f"EXPR {expr} {mode} {result} {datetime.now()}\n")

    return jsonify({
        "expression": expr,
        "mode": mode,
        "result": result
    })


# -------------------------
# API Documentation
# -------------------------

@app.route('/docs')
def docs():
    return """
    <h2>Cloud Trigonometric API Documentation</h2>

    <h3>Basic Evaluation</h3>
    /api/v1/evaluate?op=sin&value=30&mode=degree

    <h3>Complex Expression</h3>
    /api/v1/expression?expr=tan(30)^2+sin(30)

    <h3>Examples</h3>

    tan(30)^2 + sin(30)
    sin(30) + cos(60)
    sqrt(25) + sin(30)
    log(10) + cos(60)

    <h3>Operations Supported</h3>
    sin cos tan sqrt log

    <h3>Modes</h3>
    degree | radian
    """


# -------------------------
# HISTORY API
# -------------------------

@app.route('/api/v1/history')
def get_history():
    return jsonify(history)


# -------------------------
# HEALTH CHECK
# -------------------------

@app.route('/health')
def health():
    return jsonify({"status": "service running"})


# -------------------------
# RUN SERVER
# -------------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)