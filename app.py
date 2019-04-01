# -*- coding: utf-8 -*-
from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
from sklearn.externals import joblib
model = joblib.load('model.pkl')


app = Flask(__name__)


# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- 


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    #col = ['age', 'mealsperday', 'readingbook', 'checkingbook', 'parent_teacher']
    #data= np.array([meals_data, age, reading, checkbook, gender, parent_teacher])
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        meals = request.form['meals']
        book = request.form['book']
        check_book = request.form['check_book']
        parent_teacher = request.form['parent_teacher']
        new_age = age.split('-')
        year_born = int(new_age[0])
        age = 2019-year_born
        gender = int(gender);meals=int(meals);book=int(book)
        check_book = int(check_book);parent_teacher=int(parent_teacher)

        data = [[meals, age, book, check_book, gender, parent_teacher]] 
        predicted = model.predict(data)
        predicted = predicted[0]
        print(predicted)
        print(gender, age , meals, book, check_book, parent_teacher)
        return render_template("pred.html", prediction = predicted)


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(debug=True, use_reloader=True)
