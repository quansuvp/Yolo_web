from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .import db
from random import randint
import json
SOTRAGE1 = 'res1.txt'
SOTRAGE2 = 'res2.txt'
SOTRAGE4 = 'res4.txt'

views = Blueprint('views',__name__)

def read_numbers(file_path):
    try:
        # Read the entire content of the file
        with open(file_path, 'r') as file:
            content = file.read().strip()

        # Extract numbers from the content
        numbers = [int(num) for num in content.split() if num.isdigit()]

        return numbers
    except FileNotFoundError:
        return None


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note= request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user = current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({'success': True})

@views.route('/dashboard',methods=['GET','POST'])
def dashboard():
    #* Chuyen data vao day de pass qua frontend
        #* các phương thức lấy data thực thi ở đây rồi truyền vào 4 biến ở dưới 
    #* Luu vao data base thì dùng db.sesion.add + db.session.commit()
    return render_template('dashboard.html',user = current_user)



@views.route('/dashboardupdate',methods=['GET','POST'])
def get_sensor_reading():
    #* Chuyen data vao day de pass qua frontend
        #* các phương thức lấy data thực thi ở đây rồi truyền vào 4 biến ở dưới 
    temperature = read_numbers(SOTRAGE1)
    pressure = 1
    humidity = read_numbers(SOTRAGE2)
    light = read_numbers(SOTRAGE4)
    #* Luu vao data base thì dùng db.sesion.add + db.session.commit()
    # data =(temperature,pressure,humidity,light)
    # return render_template('dashboard.html',user = current_user,data=data)
    return jsonify({
        'temperature':temperature,
        'pressure':pressure,
        'humidity':humidity,
        'light':light,
    })