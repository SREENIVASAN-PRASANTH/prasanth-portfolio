from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database initialization
def init_db():
    os.makedirs('instance', exist_ok=True)
    with sqlite3.connect('instance/portfolio.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                published BOOLEAN DEFAULT 1
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create default admin user
        admin_email = "prasanth_2003@outlook.com"
        admin_password = generate_password_hash("admin123")  # Change this password
        admin_name = "Prasanth S"

        try:
            conn.execute(
                "INSERT INTO admin (email, password_hash, name) VALUES (?, ?, ?)",
                (admin_email, admin_password, admin_name)
            )
        except sqlite3.IntegrityError:
            pass  # Admin already exists

# Portfolio data from updated resume
portfolio_data = {
    'personal_info': {
        'name': 'PRASANTH S',
        'title': 'Software Developer',
        'email': 'prasanth_2003@outlook.com',
        'phone': '+91-9444575820',
        'location': 'Chennai',
        'linkedin': 'linkedin.com/in/s-prasanth2003',
        'github': 'github.com/SREENIVASAN-PRASANTH',
        'summary': 'Computer Science graduate with strong Python development skills in building web applications and RESTful APIs. Proficient in frameworks like Flask and version control using Git. Solid problem-solving ability and hands-on experience through projects.'
    },
    'education': {
        'degree': 'B.E. Computer Science & Engineering',
        'cgpa': '8.3 CGPA',
        'college': 'Vel Tech High Tech Engineering College',
        'intermediate': {
            'course': 'Intermediate or 12th, Computer Science',
            'percentage': '87.4%',
            'school': 'Kendriya Vidyalaya C.R.P.F., Avadi'
        },
        'secondary': {
            'course': 'Senior Secondary School or 10th',
            'percentage': '88.6%',
            'school': 'Kendriya Vidyalaya C.R.P.F., Avadi'
        }
    },
    'experience': {
        'position': 'Web Development Intern',
        'company': 'BuildHr Management Consultants Private Limited',
        'responsibilities': [
            'Coordinated with vendor, management, and stakeholders for the development of new products website.',
            'Created custom billing templates using HTML and CSS which are further used by senior developers to automate it via Zoho creator.',
            'Identified and documented the bugs in the products website and also communicated them to the vendor for resolution.'
        ]
    },
    'projects': [
        {
            'name': 'BEAR TRACKING APPLICATION',
            'description': 'Developed a Salesforce app using LWC to track and display bear locations on a map. Used Lightning Message Service (LMS) for cross-component communication and dynamic UI updates.',
            'technologies': ['LWC', 'Apex', 'Lightning Map', 'LMS', 'Lightning Data Service'],
            'github': 'https://github.com/SREENIVASAN-PRASANTH'
        },
        {
            'name': 'CONTACT MANAGEMENT APP',
            'description': 'Built a custom Salesforce app to search for Accounts and manage related Contacts. Users can view, add, edit, and delete contacts linked to an account using a dynamic UI built with LWC and Apex.',
            'technologies': ['LWC', 'Apex', 'SOQL', 'Custom Events'],
            'github': 'https://github.com/SREENIVASAN-PRASANTH'
        },
        {
            'name': 'VOICE ASSISTANT',
            'description': 'Developed a voice-controlled assistant that listens to user queries, processes them using the Gemini AI model, and responds with synthesized speech. Integrated speech recognition and text-to-speech for voice interaction.',
            'technologies': ['Python', 'Pyttsx3', 'Speech Recognition', 'Gemini AI'],
            'github': 'https://github.com/SREENIVASAN-PRASANTH'
        },
        {
            'name': 'MAIL SPAM DETECTOR',
            'description': 'Built and deployed a web application that classifies emails as spam or not using a pre-trained ML model. Implemented both UI-based Interface and a RESTful API for classification.',
            'technologies': ['Python', 'Scikit-learn', 'Flask'],
            'github': 'https://github.com/SREENIVASAN-PRASANTH'
        }
    ],
    'skills': {
        'salesforce': ['Apex', 'LWC', 'SOQL'],
        'frontend': ['HTML5', 'CSS3', 'Bootstrap', 'JavaScript'],
        'backend': ['Python', 'Java (Learning - OOP: Inheritance, Polymorphism, Data Types)'],
        'database': ['MySQL'],
        'version_control': ['Git'],
        'soft_skills': ['Adaptability', 'Analytical thinking', 'Team player']
    },
    'certifications': [
        {
            'provider': 'NxtWave Certifications',
            'courses': ['HTML5', 'CSS3', 'Bootstrap', 'JavaScript', 'Python']
        },
        {
            'provider': 'NPTEL Online Certification',
            'courses': ['Python for Data Science']
        },
        {
            'provider': 'Udemy Certifications',
            'courses': ['Learn Salesforce (Admin + Developer) with LWC Live Project']
        }
    ],
    'achievements': [
        'Led and coordinated a team of 3 to conduct the "Scramble Code" coding event with 40+ participants as part of the department technical fest.'
    ]
}

@app.route('/')
def index():
    return render_template('index.html', data=portfolio_data)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Save to database
        with sqlite3.connect('instance/portfolio.db') as conn:
            conn.execute(
                "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
                (name, email, subject, message)
            )

        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('index') + '#contact')

# Blog routes
@app.route('/blogs')
def blogs():
    with sqlite3.connect('instance/portfolio.db') as conn:
        posts = conn.execute(
            "SELECT * FROM blog_posts WHERE published = 1 ORDER BY created_at DESC"
        ).fetchall()
    return render_template('blogs.html', posts=posts, data=portfolio_data)

@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    with sqlite3.connect('instance/portfolio.db') as conn:
        post = conn.execute(
            "SELECT * FROM blog_posts WHERE id = ? AND published = 1", (post_id,)
        ).fetchone()
    if not post:
        flash('Blog post not found.', 'error')
        return redirect(url_for('blogs'))
    return render_template('blog_detail.html', post=post, data=portfolio_data)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('instance/portfolio.db') as conn:
            admin = conn.execute(
                "SELECT * FROM admin WHERE email = ?", (email,)
            ).fetchone()

        if admin and check_password_hash(admin[2], password):
            session['admin_id'] = admin[0]
            session['admin_name'] = admin[3]
            flash('Welcome back!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'error')

    return render_template('admin_login.html', data=portfolio_data)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    with sqlite3.connect('instance/portfolio.db') as conn:
        posts = conn.execute(
            "SELECT * FROM blog_posts ORDER BY created_at DESC"
        ).fetchall()

        messages = conn.execute(
            "SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 10"
        ).fetchall()

    return render_template('admin_dashboard.html', posts=posts, messages=messages, data=portfolio_data)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
def admin_new_blog():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        published = 'published' in request.form

        with sqlite3.connect('instance/portfolio.db') as conn:
            conn.execute(
                "INSERT INTO blog_posts (title, content, published) VALUES (?, ?, ?)",
                (title, content, published)
            )

        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_blog_form.html', data=portfolio_data)

@app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
def admin_edit_blog(post_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    with sqlite3.connect('instance/portfolio.db') as conn:
        post = conn.execute(
            "SELECT * FROM blog_posts WHERE id = ?", (post_id,)
        ).fetchone()

    if not post:
        flash('Blog post not found.', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        published = 'published' in request.form

        with sqlite3.connect('instance/portfolio.db') as conn:
            conn.execute(
                "UPDATE blog_posts SET title = ?, content = ?, published = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (title, content, published, post_id)
            )

        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_blog_form.html', post=post, data=portfolio_data)

@app.route('/admin/blog/delete/<int:post_id>')
def admin_delete_blog(post_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    with sqlite3.connect('instance/portfolio.db') as conn:
        conn.execute("DELETE FROM blog_posts WHERE id = ?", (post_id,))

    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

