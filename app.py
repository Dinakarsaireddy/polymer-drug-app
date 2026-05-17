from flask import Flask, render_template, request, redirect
from config import db

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']

    cursor=db.cursor()

    query="SELECT * FROM users WHERE username=%s AND password=%s"

    cursor.execute(query,(username,password))
    user=cursor.fetchone()

    if user:
        return redirect('/dashboard')
    
    return "invalid login"


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/addpage')
def addpage():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_drug():
    drug= request.form['drug']
    polymer=request.form['polymer']
    solubility=request.form['solubility']
    release=request.form['release']
    circulation=request.form['circulation']

    cursor = db.cursor()

    query="""
    INSERT INTO drugs
    (drug_name, polymer_name, solubility, release_time, circulation_time)
    VALUES (%s,%s,%s,%s,%s)
    """

    values= (drug,polymer, solubility,release,circulation)
    cursor.execute(query,values)
    db.commit()

    return "Drug data saved successfully"

@app.route('/view')
def view_drugs():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM drugs")

    drugs = cursor.fetchall()

    return render_template('view.html', drugs=drugs)



@app.route('/search', methods=['POST'])
def search():

    keyword = request.form['keyword']

    cursor = db.cursor()

    query = "SELECT * FROM drugs WHERE drug_name LIKE %s"

    cursor.execute(query, ('%' + keyword + '%',))

    drugs = cursor.fetchall()

    return render_template('view.html', drugs=drugs)

@app.route('/delete/<int:id>')
def delete_drug(id):

    cursor = db.cursor()

    query = "DELETE FROM drugs WHERE id=%s"

    cursor.execute(query, (id,))

    db.commit()

    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)
