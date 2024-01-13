from flask import Flask, render_template

app = Flask(__name__, template_folder='../Frontend/html' ,  static_folder='../Frontend/css')

@app.route('/')
def hone():
    return render_template('index.html')



@app.route('/login')
def sigin():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)