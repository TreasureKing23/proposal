from flask import Flask, render_template, g,request,redirect,url_for
import sqlite3

app = Flask(__name__)

PE_MIN = 85
INVIG_MIN = 70

DATABASE = 'testdb'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/schools')
def schoolpage():
    db = get_db()
    query = 'SELECT SchoolCode, Name, Region FROM Schools'
    schools = db.execute(query).fetchall()
    return render_template('schools.html',schools=schools)

@app.route('/add-school', methods=['GET','POST'])
def add_school():
    db = get_db()
    if request.method == "POST":
        school_code=request.form['school_code']
        name=request.form['name']
        region=request.form['region']

        
        db.execute('INSERT INTO Schools(SchoolCode, Name, Region) VALUES (?, ?, ?)',
                   (school_code,name,region))
        db.commit()
        return redirect(url_for('schoolpage'))
    
    regions = db.execute('SELECT Number, Name FROM Region').fetchall()
    return render_template('add_school.html', regions=regions)

@app.route('/examiners')
def examinerpage():
    db = get_db()
    query = 'SELECT * FROM Examiners'
    ex = db.execute(query).fetchall()
    return render_template('examiners.html', examiners = ex)

@app.route('/add-examiners', methods=['GET','POST'])
def add_examiner():
    db = get_db()
    if request.method == "POST":
        name= request.form['name']
        address = request.form['address']
        contactnumber = request.form['number']
        rank = request.form['rank']
        status=request.form['status']
        region=request.form['region']
    
        db.execute('INSERT INTO Examiners(Name, Address,ContactNumber,Rank,Status, Region) VALUES (?, ?, ?, ?, ?, ?)',(name,address,contactnumber,rank,status,region))
        db.commit()
        return redirect(url_for('examinerpage'))

    regions = db.execute('SELECT Number, Name FROM Region').fetchall()
    ranks = db.execute('SELECT Rank FROM Role').fetchall()
    statuses = db.execute('SELECT Type FROM Status').fetchall()
    return render_template('add_examiners.html', regions=regions, ranks=ranks, statuses = statuses)

@app.route('/assessment', methods=['GET','POST'])
def assessmentpage():
    db = get_db()
    query = 'SELECT * FROM Assessment'
    ass = db.execute(query).fetchall()
    return render_template('assessment.html', assessments = ass)

@app.route('/input_scores', methods =['GET','POST'])
def inputpage():
    db = get_db()


    ranks = db.execute('SELECT * FROM Role').fetchall()
    statuses = db.execute('SELECT Type FROM Status').fetchall()


if __name__ == '__main__':
    app.run(debug=True)
