from flask import Flask, render_template, request
from config import db

app = Flask(__name__)

@app.route('/')
def home():
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

if __name__ == '__main__':
    app.run(debug=True)
