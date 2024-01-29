from flask import Flask, request, session, url_for, redirect, render_template
from APP.apply_model import predictor
from APP.db import create_connection, check_credintials, add_prediction_information, display_DL_model_data, clear_table
from APP.wtf_model import LoginForm, PredictionForm
import pandas as pd
import os

app = Flask(__name__, static_url_path='/APP/static')
app.config['SECRET_KEY'] = "azeazeazdqsdsdfq545q4"
app.config['UPLOAD_FOLDER'] = 'static'
app.config['COLS'] = ['Id', 'Model_name', 'Prediction date', 'Prediction', 'Error']

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/page')
def page():
    form = PredictionForm()
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = create_connection('database/sqlite.db')
    table = display_DL_model_data(conn)
    df = pd.DataFrame(table, columns=app.config['COLS'])
    table = df.to_html(index=False)
    return render_template('page.html', form=form, table=table)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        conn = create_connection('database/sqlite.db')
        # Assuming you have some logic to check the login credentials
        if check_credintials(conn, form.username.data, form.password.data):
            # If login is successful, redirect to the 'page.html'
            session['logged_in'] = True
            return redirect(url_for('page'))
        else:
            # If login fails, you might want to render the 'index.html' again or show an error message
            message = f'Your password or username are incorrect, please check them.'
            return render_template('index.html', error_message=message,  form=form)

    # If it's a GET request, simply render the login page
    return render_template('index.html', form=form)

@app.route('/delete_all_records', methods=['POST'])
def delete_all_records():
    form = PredictionForm()
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = create_connection('database/sqlite.db')
    clear_table(conn)

    table = display_DL_model_data(conn)
    df = pd.DataFrame(table, columns=app.config['COLS'])
    table = df.to_html(index=False)

    return render_template('page.html', table=table, form=form)

@app.route('/predict', methods=['GET','POST'])
def predict():
    form = PredictionForm()
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if form.validate_on_submit():
        conn = create_connection('database/sqlite.db')
        selected_model = form.model.data
        file = form.file.data
        
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
                                   error=prediction_result.get('Error'))
        
        table = display_DL_model_data(conn)
        df = pd.DataFrame(table, columns=app.config['COLS'])
        table = df.to_html(index=False)

        # Pass the prediction result to the HTML template
        return render_template('page.html', 
                               data_image=img_path_to_save,
                               table=table,
                                form=form,
                               prediction=vegetables)
    
    return render_template('page.html',  form=form)
