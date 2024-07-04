#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


# In[3]:


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'


# In[4]:


def insert_sample_data():
    sample_students = [
        {"first_name": "Alice", "last_name": "Smith", "dob": "2000-01-01", "amount_due": 100.0},
        {"first_name": "Bob", "last_name": "Johnson", "dob": "2001-02-02", "amount_due": 200.0},
        {"first_name": "Charlie", "last_name": "Williams", "dob": "2002-03-03", "amount_due": 300.0},
        {"first_name": "David", "last_name": "Brown", "dob": "2003-04-04", "amount_due": 400.0},
        {"first_name": "Eva", "last_name": "Jones", "dob": "2004-05-05", "amount_due": 500.0},
        {"first_name": "Frank", "last_name": "Garcia", "dob": "2005-06-06", "amount_due": 600.0},
        {"first_name": "Grace", "last_name": "Martinez", "dob": "2006-07-07", "amount_due": 700.0},
        {"first_name": "Henry", "last_name": "Davis", "dob": "2007-08-08", "amount_due": 800.0},
        {"first_name": "Ivy", "last_name": "Rodriguez", "dob": "2008-09-09", "amount_due": 900.0},
        {"first_name": "Jack", "last_name": "Miller", "dob": "2009-10-10", "amount_due": 1000.0}
    ]

    for student in sample_students:
        new_student = Student(
            first_name=student['first_name'],
            last_name=student['last_name'],
            dob=datetime.strptime(student['dob'], '%Y-%m-%d').date(),
            amount_due=student['amount_due']
        )
        db.session.add(new_student)
    db.session.commit()


# In[5]:


with app.app_context():
    db.create_all()


# In[6]:


@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
        amount_due=data['amount_due']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully'}), 201


# In[7]:


@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = []
    for student in students:
        student_data = {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'amount_due': student.amount_due
        }
        result.append(student_data)
    return jsonify(result)


# In[8]:


@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    student_data = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': student.amount_due
    }
    return jsonify(student_data)


# In[9]:


@app.route('/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
    student.amount_due = data['amount_due']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})


# In[10]:


@app.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})


# In[ ]:


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


# In[ ]:




