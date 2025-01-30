**README for Air Pollution Prediction Application**

---

### **Project Overview**
This application is designed to predict air pollution levels based on user inputs such as year, month, and production tons. It utilizes a machine learning model to generate predictions and provides a user-friendly interface for registration, login, and data visualization.

### **Features**
- User registration and login functionality.
- Input form for predicting air pollution levels.
- Display of prediction results including various air quality parameters.
- Ability to save prediction results to an Excel file.
- Visualization of prediction results using charts.

### **Technologies Used**
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Data Processing:** Pandas
- **Machine Learning:** Scikit-learn
- **Charting:** Chart.js

### **Installation Instructions**
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Initialization**
   - The application will automatically create a SQLite database (`users.db`) upon the first run.

5. **Run the Application**
   ```bash
   python app.py
   ```
   - Open your web browser and navigate to `http://127.0.0.1:5000`.

### **Usage Instructions**
1. **Register an Account**
   - Navigate to the registration page and fill in the required fields (email, username, password).

2. **Login**
   - Use your registered credentials to log in.

3. **Make Predictions**
   - After logging in, you can input the year, month, and production tons to get predictions on air pollution levels.

4. **View Results**
   - The results will be displayed on a new page, and you can choose to save them to an Excel file.

5. **Logout**
   - You can log out from any page to end your session.


