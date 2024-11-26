# import the neccessary modules
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS

# Create an app instance
app = Flask(__name__)
CORS(app)

### Create a database.
### It is an SQLite Database
### Import, connect, Create Table, Execute and Close

# Import
import sqlite3 
# connect
database = sqlite3.connect('data.sqlite')
# Make a query of creating a table
create_table = """CREATE TABLE IF NOT EXISTS student (
                id integer PRIMARY KEY,
                'first name' text NOT NULL,
                'last name' text NOT NULL,
                age integer NOT NULL,
                gender text NOT NULL
                )"""
# Execute
database.execute(create_table)
#close database
database.close()

# Create a home page route
@app.route('/')
def home():
    return("This is Adesina's API")

# Create a POST route
@app.route('/create', methods=['POST'])
def create():
    # 1. connect database
    database = sqlite3.connect('data.sqlite')
    # 2. get information from the frontend
    first_name_py = request.form.get('first name')
    last_name_py = request.form.get('last name')
    age_py = request.form.get('age')
    gender_py = request.form.get('gender')
    # 3. Make a Write query to store the information in the database
    write_info = """INSERT INTO student ('first name', 'last name', age, gender) 
                                        VALUES (?, ?, ? , ?)"""
    # 4. Execute the write query
    database.execute(write_info, (first_name_py, last_name_py, age_py, gender_py))
    # 5. Commit the database
    database.commit()
    # 6. close database
    database.close()
    # 7. return 
    # return jsonify({"status": "Success"})
    return redirect(url_for('read'))

# Create a GET route
@app.route('/read')
def read():
    # 1. connect database
    database = sqlite3.connect('data.sqlite')
    # 2. make query to fetch all information in the database
    read_all = """SELECT * FROM student"""
    # 3. exceute
    read_all_execute = database.execute(read_all)
    # 4. fetchall
    fetch_data = read_all_execute.fetchall()
    
    #conver the fetched data to a list of dictionaries
    students_list = []
    for student in fetch_data:
        students_list.append({ 
            'id': student[0], 
            'first name': student[1], 
            'last name': student[2], 
            'age': student[3], 
            'gender': student[4]
        })
    # 5. convert the informaion to json format and return
    return jsonify({
        "status": "success",
        "students": students_list
    })

# Run the app
if __name__ == '__main__':
    app.run(port=8000, debug=True)
