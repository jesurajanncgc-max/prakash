from flask import Flask, render_template, request, jsonify
from sympy import symbols, diff, integrate, sin, cos, tan, cot, sec, csc, sympify, Matrix, solve

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json.get('code', '')
    lines = data.strip().split('\n')
    output = []
    
    x, y, z = symbols('x y z')

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            # Addition for multiple numbers
            if line.startswith("add:"):
                parts = line[4:].split(',')
                numbers = [float(p.strip()) for p in parts]
                result = sum(numbers)
                output.append(f"Result: {result}")

            # Subtraction for multiple numbers
            elif line.startswith("sub:"):
                parts = line[4:].split(',')
                numbers = [float(p.strip()) for p in parts]
                result = numbers[0]
                for num in numbers[1:]:
                    result -= num
                output.append(f"Result: {result}")

            # Multiplication for multiple numbers
            elif line.startswith("mul:") or line.startswith("multiply:"):
                prefix_len = 4 if line.startswith("mul:") else 9
                parts = line[prefix_len:].split(',')
                numbers = [float(p.strip()) for p in parts]
                result = 1.0
                for num in numbers:
                    result *= num
                output.append(f"Result: {result}")

            # Division for multiple numbers
            elif line.startswith("div:") or line.startswith("divide:"):
                prefix_len = 4 if line.startswith("div:") else 7
                parts = line[prefix_len:].split(',')
                numbers = [float(p.strip()) for p in parts]
                result = numbers[0]
                for num in numbers[1:]:
                    if num == 0:
                        raise ValueError("Division by zero error")
                    result /= num
                output.append(f"Result: {result}")

            # Advanced Differentiation (Algebraic & Trigonometric)
            elif line.startswith("diff:"):
                expr_str = line[5:].strip()
                expr = sympify(expr_str)
                result = diff(expr, x)
                output.append(f"Result: {result}")

            # Advanced Integration (Algebraic & Trigonometric)
            elif line.startswith("integrate:"):
                expr_str = line[10:].strip()
                expr = sympify(expr_str)
                result = integrate(expr, x)
                output.append(f"Result: {result} + C")

            # Trigonometric Expressions & Combinations (sin(x) + cos(x), sin(x)/cos(x), etc.)
            elif line.startswith("trig:"):
                expr_str = line[5:].strip()
                expr = sympify(expr_str)
                output.append(f"Result: {expr}")

            # Matrix Operations
            elif line.startswith("matrix:"):
                mat_str = line[7:].strip()
                mat = Matrix(eval(mat_str))
                output.append(f"Result: {mat}")

            # Determinant Calculation
            elif line.startswith("det:"):
                mat_str = line[4:].strip()
                mat = Matrix(eval(mat_str))
                result = mat.det()
                output.append(f"Result: {result}")

            # Solving Linear Equations
            elif line.startswith("solve:"):
                eq_str = line[6:].strip()
                if "=" in eq_str:
                    lhs, rhs = eq_str.split("=")
                    eq = sympify(lhs) - sympify(rhs)
                else:
                    eq = sympify(eq_str)
                result = solve(eq, x)
                output.append(f"Result: {result}")

            else:
                output.append(f"Error: Unknown command '{line}'")
                
        except Exception as e:
            output.append(f"Error: {str(e)}")
            
    return jsonify(output=output)

if __name__ == '__main__':
    app.run(debug=True)
