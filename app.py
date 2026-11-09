from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json.get('code', '')
    output = []
    
    lines = data.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            if line.startswith("add:"):
                parts = line[4:].split(',')
                n1 = float(parts[0].strip())
                n2 = float(parts[1].strip())
                output.append(f"Result: {n1 + n2}")
                
            elif line.startswith("sub:"):
                parts = line[4:].split(',')
                n1 = float(parts[0].strip())
                n2 = float(parts[1].strip())
                output.append(f"Result: {n1 - n2}")
                
            elif line.startswith("multiply:"):
                parts = line[9:].split(',')
                n1 = float(parts[0].strip())
                n2 = float(parts[1].strip())
                output.append(f"Result: {n1 * n2}")
                
            elif line.startswith("divide:"):
                parts = line[7:].split(',')
                n1 = float(parts[0].strip())
                n2 = float(parts[1].strip())
                if n2 == 0:
                    output.append("Error: Division by zero is not allowed")
                else:
                    output.append(f"Result: {n1 / n2}")
                    
            elif line.startswith("integrate:"):
                expr = line[10:].strip()
                if 'x^' in expr:
                    power = float(expr.split('^')[1])
                    new_power = power + 1
                    output.append(f"Result: (x^{new_power}) / {new_power} + C")
                else:
                    output.append("Error: Use format like integrate: x^2")
                    
            elif line.startswith("differentiate:"):
                expr = line[14:].strip()
                if 'x^' in expr:
                    power = float(expr.split('^')[1])
                    new_power = power - 1
                    output.append(f"Result: {power}x^{new_power}")
                else:
                    output.append("Error: Use format like differentiate: x^3")
                    
            else:
                output.append(f"Error: Command not recognized -> '{line}'")
                
        except Exception as e:
            output.append(f"Error executing line '{line}': Invalid syntax")
            
    return jsonify({'output': '\n'.join(output)})

if __name__ == '__main__':
    app.run(debug=True)