import os
from flask import Flask, render_template, request, redirect, session
from model import users, jobs, applications

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        users[email] = {'password': password, 'role': role}
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            session['role'] = user['role']
            return redirect('/admin_dashboard' if user['role'] == 'admin' else '/job_list')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/job_list')
def job_list():
    if 'user' not in session or session.get('role') != 'user':
        return redirect('/login')
    return render_template('job_list.html', jobs=jobs)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if 'user' not in session or session.get('role') != 'user':
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        resume = request.files['resume']
        filename = os.path.join('static/uploads', resume.filename)
        resume.save(filename)
        applications.append({'job_id': job_id, 'name': name, 'resume': filename})
        return "Application submitted!"
    return render_template('apply.html', job_id=job_id)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin_dashboard.html', jobs=jobs, applications=applications)

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)
