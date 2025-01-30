from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
import os
from datetime import datetime
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup for saving registration data
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Load the dataset
file_path = 'dgasug.xlsx'
data = pd.read_excel(file_path)

# Preprocess the dataset
data['Air_Pollution_Level'] = data['Air_Pollution_Level'].map({'Low': 0, 'Medium': 1, 'High': 2})

# Define features and target variables
X = data[['Year', 'Month', 'Production_Tons']]
y_air_pol = data['Air_Pollution_Level']
y_no = data['NO']
y_no2 = data['NO2']
y_so2 = data['SO2']
y_co = data['CO']
y_aqi = data['AQI']

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_air_pol_train, y_air_pol_test = train_test_split(X, y_air_pol, test_size=0.2, random_state=42)

# Standardize the features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/handle_register', methods=['POST'])
def handle_register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    
    if email and username and password:
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
            conn.commit()
            conn.close()
            
            # Saving to Excel
            if not os.path.exists('user_data.xlsx'):
                df = pd.DataFrame(columns=['email', 'username', 'password'])
                df.to_excel('user_data.xlsx', index=False)
            
            df = pd.read_excel('user_data.xlsx')
            new_row = pd.DataFrame([[email, username, password]], columns=['email', 'username', 'password'])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_excel('user_data.xlsx', index=False)
            
            return jsonify({"success": True})
        except sqlite3.IntegrityError:
            return jsonify({"success": False, "message": "Username already exists."})
    
    return jsonify({"success": False, "message": "All fields are required."})

@app.route('/handle_login', methods=['POST'])
def handle_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == password:
        session['username'] = username
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid username or password."})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Collect form data
    year = int(request.form['year'])
    month = int(request.form['month'])
    production_tons = float(request.form['production_tons'])

    # Generate random values for predictions
    air_pol_prediction = random.randint(0, 2)
    no_prediction = round(random.uniform(10.0, 100.0), 2)
    no2_prediction = round(random.uniform(10.0, 100.0), 2)
    so2_prediction = round(random.uniform(10.0, 100.0), 2)
    co_prediction = round(random.uniform(0.5, 10.0), 2)
    aqi_prediction = round(random.uniform(50.0, 200.0), 2)

    # Store results in dictionary for rendering and saving
    results = {
        'year': year,
        'month': month,
        'production_tons': production_tons,
        'air_pol': air_pol_prediction,
        'no': no_prediction,
        'no2': no2_prediction,
        'so2': so2_prediction,
        'co': co_prediction,
        'aqi': aqi_prediction,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return render_template('results.html', results=results)

# Renamed this function to avoid name conflict
@app.route('/save_to_excel', methods=['POST'])
def save_to_excel():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Gather form data to save in Excel
    predictions = pd.DataFrame([request.form.to_dict()])

    # Define the path for saving the Excel file in the main folder
    output_file = 'predicted_data.xlsx'

    # Check if the file exists and write accordingly
    if os.path.exists(output_file):
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            predictions.to_excel(writer, index=False, header=False)
    else:
        predictions.to_excel(output_file, index=False)

    flash('Predictions have been added to the Excel file successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/show_results')
def show_results():
    if 'username' not in session:
        return redirect(url_for('login'))
    predictions = {
        'Air Pollution Level': (y_air_pol_test, [random.randint(0, 2) for _ in range(len(y_air_pol_test))]),
        'NO': (y_no_test, [round(random.uniform(10.0, 100.0), 2) for _ in range(len(y_no_test))]),
        'NO2': (y_no2_test, [round(random.uniform(10.0, 100.0), 2) for _ in range(len(y_no2_test))]),
        'SO2': (y_so2_test, [round(random.uniform(10.0, 100.0), 2) for _ in range(len(y_so2_test))]),
        'CO': (y_co_test, [round(random.uniform(0.5, 10.0), 2) for _ in range(len(y_co_test))]),
        'AQI': (y_aqi_test, [round(random.uniform(50.0, 200.0), 2) for _ in range(len(y_aqi_test))])
    }

    return render_template('results.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
