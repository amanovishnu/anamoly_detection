import joblib
import numpy as np
import pandas as pd
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/model')
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route("/model")
def model():
    return render_template("model.html")


@app.route("/predict_anomaly", methods=['POST'])
def predict_anomaly():
    if request.method == 'POST':
        model = joblib.load('./pickle_file/model.pkl')
        data = request.get_json()
        df = pd.DataFrame([data.values()], columns=data.keys())
        df['FLAG_SF'] = df['FLAG_SF'].astype(bool)
        data = df.iloc[0].values.tolist()
        input_data = np.array(data).reshape(1, -1)
        output = model.predict(input_data)
        response = {
            "status": "success",
            "output": int(output[0])
        }
        return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
