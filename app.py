from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la plantilla index.html
    return render_template('index.html')

@app.route('/login.html')
def login():
    # Renderiza la plantilla login.html
    return render_template('login.html')

@app.route('/register.html')
def register():
    # Renderiza la plantilla register.html
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
