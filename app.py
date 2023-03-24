"""
1. Paypal API Crap
3. bring it to younglinguists.net
"""
from flask import Flask, render_template, request, redirect, url_for, session, abort
import json
app = Flask(__name__)
app.secret_key = "|\|||<|-|||_"

@app.route('/', methods=['GET', 'POST'])
def home():
    if session:
        with open('student.json') as js3:
            student2 = json.load(js3)
            if session['email'] in student2['people']:
                return redirect(url_for('therealclasspage'))
            else:
                return render_template('home.html')
    else:
        return render_template('home.html')
            
@app.route('/#')
def homeigidk():
    return render_template('home.html')

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    lang = request.form['lang']
    return render_template('pay.html', lang=lang)

@app.route('/money', methods=['GET', 'POST'])
def money():
    name = request.form['name']
    psw= request.form['psw']
    grade = request.form['grade']
    timeDay = request.form['timeDay']
    lang = request.form['lang']
    email = request.form['email']
    return render_template('money.html', name=name, grade=grade, timeDay=timeDay, lang=lang, email=email, psw=psw)

@app.route('/finalize', methods=['GET'])
def final():
    with open('student.json') as js3:
        student1 = json.load(js3)
    with open('count.json') as c1:
        count1 = json.load(c1)
    with open('db.json') as js1:
        user_dict1 = json.load(js1)
        id = count1['userCount'] + 1
        name = session['name']
        grade = session['grade']
        timeDay = session['timeDay']
        lang = session['lang']
        email = session['email']
        psw = session['psw']
        if email in student1['people']:
            if lang in user_dict1[elm]['lang']:
                a=6920
            else:
                for elm in user_dict1.keys():
                    user_dict1[elm]['lang'].append(lang)
        else:
            user_dict1[id] = {
                "name": name,
                "email": email,
                "grade": grade,
                "timeDay": timeDay,
                "lang": [lang],
                "psw": psw
            }
            count1['userCount'] += 1
            student1['people'].append(email)
        with open('count.json', 'w') as idc:
            json.dump(count1, idc)
        with open('db.json', 'w') as idk:
            json.dump(user_dict1, idk)
        with open('student.json', 'w') as urmom:
            json.dump(student1, urmom)
            return redirect(url_for('home'))

@app.route("/pending", methods=["POST", "GET"])
def pending():
    name = request.form['name']
    grade = request.form['grade']
    timeDay = request.form['timeDay']
    lang = request.form['lang']
    email = request.form['email']
    psw = request.form['psw']
    session['name'] = name
    session['grade'] = grade
    session['timeDay'] = timeDay
    session['email'] = email
    session['lang'] = lang
    session['psw'] = psw
    return redirect(url_for('homeigidk'))

@app.route('/backend/userData', methods=['GET', 'POST'])
def userData():
    with open('db.json') as js1:
        json1 = json.load(js1)
        return render_template('data.html', json1=json1)
        #return json1

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', msg="n")

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    email = request.form['email']
    psw = request.form['psw']
    with open('student.json') as file:
        j1 = json.load(file)
        if email in j1['people']:
            with open('db.json') as file2:
                j2 = json.load(file2)
                for elm in j2.keys():
                    if j2[elm]['psw'] == psw:
                        session.clear()
                        session['name'] = j2[elm]['name']
                        session['email'] = j2[elm]['email']
                        session['psw'] = j2[elm]['psw']
                        session['lang'] = j2[elm]['lang']
                        session['grade'] = j2[elm]['grade']
                        session['timeDay'] = j2[elm]['timeDay']
                        return redirect(url_for('home'))
                    else:
                        return render_template('login.html', msg="y")
        else:
            return render_template('login.html', msg="y")

@app.route('/session', methods=['GET', 'POST'])
def session1():
    session.clear()
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home2():

    return render_template('home2.html')

@app.route('/Home', methods=['GET', 'POST'])
def email():
    if session:
        return render_template('email.html', q='n')
    else:
        return render_template('email2.html', q='n')

@app.route('/email', methods=['GET', 'POST'])
def email2():
    msg = request.form['comments']
    email = ""
    name = ""
    try:
        email = session['email']
        name = session['name']
    except:
        email = request.form['email']
        name = request.form['name']
    with open('email.json') as file:
        j1 = json.load(file)
        with open('count.json') as file3:
            j3 = json.load(file3)
            j1[j3['emailCount']] = {
                "name": name,
                "email": email,
                "msg": msg
            }
            with open('email.json', 'w') as file1:
                json.dump(j1, file1)
            j3['emailCount'] += 1
            with open('count.json', 'w') as file2:
                json.dump(j3, file2)
            return render_template('email.html', q='y')

@app.route('/backend/emailData', methods=['GET', 'POST'])
def emailData():
    with open('email.json') as file:
        j1 = json.load(file)
        #return j1
        return render_template('emailData.html', data=j1)
    
@app.route('/dismiss', methods=['POST', 'GET'])
def dismiss():
    which = request.form['which']
    with open('email.json') as file:
        j1 = json.load(file)
        del j1[which]
        with open('email.json', 'w') as file2:
            json.dump(j1, file2)
        return redirect(url_for('emailData'))
        
@app.route('/class')
def therealclasspage():
    try:
        with open('db.json') as js4:
            student1 = json.load(js4)
            e = {}
            for elm in student1.keys():
                if student1[elm]['email'] == session['email']:
                    e = student1[elm]
            tutors = {
                "English": 'Saanvi Patil',
                "Spanish": 'Avirishi Sharma',
                "Mandarin": 'Mina Chui',
                "Marathi": 'Saanvi Patil',
                "Hindi": 'Avirishi Sharma'
            }
            zoomLinks = {
                "English": 'https://us04web.zoom.us/j/9115006875?pwd=UOFgwbDgZ2EiczLdBr7gOHBIJGora8.1',
                "Spanish": 'https://us05web.zoom.us/j/7672906617?pwd=bGQ3c2pJcXVuTEVKc0I0d3gwSzdldz09',
                "Mandarin": 'https://us05web.zoom.us/j/89036783101?pwd=RnFlRTI0aTU3cVViQmxoTjJyU1F1dz09',
                "Marathi": 'https://us04web.zoom.us/j/9115006875?pwd=UOFgwbDgZ2EiczLdBr7gOHBIJGora8.1',
                "Hindi": 'https://us05web.zoom.us/j/7672906617?pwd=bGQ3c2pJcXVuTEVKc0I0d3gwSzdldz09'
            }
            return render_template('class.html', session=e, tutors=tutors, zoomLinks=zoomLinks)
    except:
        return redirect(url_for('homeigidk'))
    
@app.route('/enroll/23427386473284693217469271346928734681723469817234691873246981327469817234')
def fillerLOL():
    try:
        return redirect(url_for('final'))
    except:
        return redirect(url_for('homeigidk'))