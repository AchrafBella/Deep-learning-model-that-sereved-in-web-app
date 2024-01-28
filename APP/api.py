from flask import Flask, request, session, url_for, redirect, render_template 
from APP.apply_model import predictor
from APP.db import create_connection, check_credintials, add_prediction_information, display_DL_model_data
import pandas as pd
import os

app = Flask(__name__, static_url_path='/APP/static')
app.config['SECRET_KEY'] = "azeazeazdqsdsdfq545q4"
app.config['UPLOAD_FOLDER'] = 'static'
app.config['COLS'] = ['Id', 'Model_name', 'Prediction date', 'Prediction', 'Error']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page')
def page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = create_connection('database/sqlite.db')
    table = display_DL_model_data(conn)
    df = pd.DataFrame(table, columns=app.config['COLS'])
    table = df.to_html(index=False)
    return render_template('page.html', table=table)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = create_connection('database/sqlite.db')
        # Assuming you have some logic to check the login credentials
        if check_credintials(conn, request.form['username'], request.form['password']):
            # If login is successful, redirect to the 'page.html'
            session['logged_in'] = True
            return redirect(url_for('page'))
        else:
            # If login fails, you might want to render the 'index.html' again or show an error message
            message = f'Your password or username are incorrect, please check them.'
            return render_template('index.html', error_message=message)

    # If it's a GET request, simply render the login page
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        conn = create_connection('database/sqlite.db')
        selected_model  = request.form.get('model')
        file = request.files.get('file')
        
        #img_path_to_render = os.path.join(app.config['UPLOAD_FOLDER'] , file.filename)
        img_path_to_save = os.path.join('APP', app.config['UPLOAD_FOLDER'] , file.filename)
        
        file.save(img_path_to_save)
        
        # Use the selected model to perform prediction
        prediction_result = predictor(selected_model , img_path_to_save)
        
        if prediction_result.get('Error'):
            vegetables = prediction_result.get('Message')
        else:
            vegetables = str(prediction_result.get('vegetables'))
        
        add_prediction_information(conn, model_name=selected_model, 
                                   prediction=vegetables, 
                                   error=bool(prediction_result.get('Error')))
        
        table = display_DL_model_data(conn)
        df = pd.DataFrame(table, columns=app.config['COLS'])
        table = df.to_html(index=False)

        # Pass the prediction result to the HTML template
        return render_template('page.html', 
                               data_image=img_path_to_save,
                               table=table,
                               prediction=vegetables)
    
    return render_template('page.html')
