from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from datetime import datetime
import logging

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        logging.debug(f"Received POST data: {data}")
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            amount_due=data['amount_due']
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student created successfully'}), 201
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return jsonify({'message': f"Missing field {e}"}), 400
    except Exception as e:
        logging.error(f"Error adding student: {e}")
        return jsonify({'message': 'Failed to create student'}), 500

@app.route('/students', methods=['GET'])
def get_students():
    try:
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
    except Exception as e:
        logging.error(f"Error fetching students: {e}")
        return jsonify({'message': 'Failed to retrieve students'}), 500

@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    try:
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
    except Exception as e:
        logging.error(f"Error fetching student: {e}")
        return jsonify({'message': 'Failed to retrieve student'}), 500

@app.route('/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        logging.debug(f"Received PUT data: {data}")
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'message': 'Student not found'}), 404

        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        student.amount_due = data['amount_due']
        db.session.commit()
        return jsonify({'message': 'Student updated successfully'})
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return jsonify({'message': f"Missing field {e}"}), 400
    except Exception as e:
        logging.error(f"Error updating student: {e}")
        return jsonify({'message': 'Failed to update student'}), 500

@app.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'message': 'Student not found'}), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'})
    except Exception as e:
        logging.error(f"Error deleting student: {e}")
        return jsonify({'message': 'Failed to delete student'}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
