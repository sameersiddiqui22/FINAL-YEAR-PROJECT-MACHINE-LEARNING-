from flask import Flask,render_template,request,redirect,url_for
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
#import jsonify
app=Flask(__name__)
cors=CORS(app)
model=pickle.load(open('LinearRegressionModel321.pkl','rb'))
car=pd.read_csv('Book111.csv')
car2=pd.read_csv('Book11.csv')
car3=pd.read_csv('newbook11.csv')
#FLASK LOGIN
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/ml-app'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
class User(db.Model):
    __tablename__ = "user1"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the database for the user
        user = User.query.filter_by(username=username).first()
        passw = User.query.filter_by(password=password).first()
        # Check if the user exists and the password is correct
        if user and passw:
            # Redirect to the index page on successful login
            return redirect(url_for('index'))
        else:
            # Handle invalid credentials
            return 'Invalid username or password'
    else:
        # Render the login form for GET requests
        return render_template('login.html')
@app.route('/index')
def index():
    return render_template('index.html')


###########################################
#Reviews
class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    car_id = db.Column(db.String(100), nullable=False)  # Assuming car name is stored in the CSV
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationships
    #user = db.relationship('user1', backref=db.backref('reviews', lazy=True))





#########################################
# @app.route('/')
# def signin():
#     return render_template('login.html')

@app.route('/model1',methods=['GET','POST'])
def model1():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('model1.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)

@app.route('/model2',methods=['GET','POST'])
def model2():
    companies=sorted(car2['company'].unique())
    car_models=sorted(car2['name'].unique())
    year=sorted(car2['year'].unique(),reverse=True)
    fuel_type=car2['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('model2.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)

@app.route('/model3',methods=['GET','POST'])
def model3():
    companies=sorted(car3['company'].unique())
    car_models=sorted(car3['name'].unique())
    year=sorted(car3['year'].unique(),reverse=True)
    suspension=car3['suspension'].unique()
    fuel_type=car3['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('model3.html',companies=companies, car_models=car_models, years=year, suspension=suspension, fuel_types=fuel_type)


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/review')
def review():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('review.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)

@app.route('/submit_review',methods=['GET','POST'])
def submit_review():
    # Get data from the request
    user_id = 2
    id = 2
     # Assuming user_id is passed in the form data
    car_id = request.form['car_model']
    rating = int(request.form['rating'])
    comment = request.form['review']

    #Create a new Review object
    new_review = Review(
        id=id,
        user_id = user_id,
        car_id=car_id,
        rating=rating,
        comment=comment,
        created_at=datetime.utcnow()
    )

    # Add the new review to the database
    db.session.add(new_review)
    db.session.commit()

    return "Review submitted"

@app.route('/reviewshow',methods=['GET','POST'])
def reviewshow():
     reviews = Review.query.all()  # Assuming you have a Review model
     return render_template('showReview.html', reviews=reviews)



@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():

    company=request.form.get('company')

    car_model=request.form.get('car_models')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=request.form.get('kilo_driven')

    prediction=model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                              data=np.array([car_model,company,year,driven,fuel_type]).reshape(1, 5)))
    print(prediction)

    return str(np.round(prediction[0],2))




model22=pickle.load(open('LinearRegressionModel333.pkl','rb'))

@app.route('/predict2',methods=['POST2'])
def predict2():
    company = request.form.get('company')

    car_model = request.form.get('car_models')
    year = request.form.get('year')
    suspension = request.form.get('suspension')
    fuel_type = request.form.get('fuel_type')

    prediction2=model22.predict(pd.DataFrame(columns=['name', 'company', 'year', 'suspension', 'fuel_type'],
                              data=np.array([car_model,company,year,suspension,fuel_type]).reshape(1, 5)))
    print(prediction2)
    return str(np.round(prediction2[0],2))





if __name__=='__main__':

    app.run()