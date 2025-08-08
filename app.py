from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB (change the URI if you're using MongoDB Atlas)
client = MongoClient("mongodb+srv://shriyakiran23:12345@project.klxhfs6.mongodb.net/")  # or replace with your MongoDB Atlas URI
db = client["Employee"]  # Use a database called "employee_db"
collection = db["Details"]  # Use a collection called "attrition_data"

# Endpoint to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    data = list(collection.find({}, {'_id': 0}))  # Exclude the _id field
    return jsonify(data)

# Endpoint to add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    new_employee = request.json  # Get the JSON data from the request
    collection.insert_one(new_employee)  # Insert it into the MongoDB collection
    return jsonify({"message": "Employee added"}), 201

# Endpoint to delete an employee by name
@app.route('/employees/<string:name>', methods=['DELETE'])
def delete_employee(name):
    # Delete employee from MongoDB where name matches
    result = collection.delete_one({"name": name})

    if result.deleted_count > 0:
        return jsonify({"message": f"Employee {name} deleted successfully"}), 200
    else:
        return jsonify({"message": f"Employee {name} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
