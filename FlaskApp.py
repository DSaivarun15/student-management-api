from flask import Flask,request,jsonify
import sqlite3

app=Flask(__name__)

def get_connection():
    conn=sqlite3.connect("students.db")
    conn.row_factory=sqlite3.Row
    return conn

@app.route("/students",methods=['GET'])
def get_students():

    conn=get_connection()
    students=conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return jsonify([dict(row) for row in students])

@app.route("/students",methods=["POST"])
def add_student():

    data=request.json

    conn=get_connection()
    conn.execute("INSERT INTO students(id,name,marks) VALUES(?,?,?)",(data["id"],data["name"],data["marks"]))

    conn.commit()
    conn.close()

    return jsonify({"message":"student added successfully"})

@app.route("/students/<int:id>",methods=["PUT"])
def update_student(id):

    data=request.json

    conn=get_connection()
    conn.execute("UPDATE students SET name=?,marks=? WHERE id=?",(data["name"],data["marks"],id))

    conn.commit()
    conn.close()

    return jsonify({"message":"student updated successfully"})

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn = get_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message":"Student deleted successfully"})

app.run(debug=True)