import os
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

# === Konfigurasi dasar ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# === Konfigurasi Flask ===
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia_kamu_ganti_sendiri'

# --- Konfigurasi database ---
DB_USER = 'root'
DB_PASSWORD = ''  # jika ada password MySQL, isi di sini
DB_HOST = 'localhost'
DB_NAME = 'portfolio_db'

# === Membuat database jika belum ada ===
import mysql.connector
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.close()
conn.close()

# === Koneksi SQLAlchemy ===
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB


db = SQLAlchemy(app)

# === Models ===
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text)
    photo = db.Column(db.String(200))

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    link = db.Column(db.String(300))

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50))
    icon = db.Column(db.String(200))

# === Forms ===
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Save')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    link = StringField('Link', validators=[Optional(), URL(message='Masukkan URL valid')])
    submit = SubmitField('Save')

class SkillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    level = StringField('Level', validators=[Optional()])
    submit = SubmitField('Save')

# === Helper ===
def save_file(file_storage):
    if not file_storage:
        return None
    filename = secure_filename(file_storage.filename)
    if filename == '':
        return None
    dest = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_storage.save(dest)
    return filename

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return fn(*args, **kwargs)
    return wrapper

# === Routes Publik ===
@app.route('/')
def index():
    user = User.query.first()
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.all()
    return render_template('index.html', user=user, projects=projects, skills=skills)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# === Login / Logout Admin ===
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['admin'] = True
            session['admin_id'] = user.id
            flash('Login berhasil', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Username atau password salah', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logout berhasil', 'info')
    return redirect(url_for('index'))

# === Dashboard Admin ===
@app.route('/admin')
@admin_required
def admin_dashboard():
    user = User.query.first()
    projects = Project.query.count()
    skills = Skill.query.count()
    return render_template('admin/dashboard.html', user=user, projects=projects, skills=skills)

# === Profile ===
@app.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    user = User.query.first()
    if not user:
        default_pw = generate_password_hash('admin123')
        user = User(username='admin', password=default_pw, name='Nama Anda', bio='Bio singkat', photo=None)
        db.session.add(user)
        db.session.commit()
    form = ProfileForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.bio = form.bio.data
        if 'photo' in request.files:
            f = request.files['photo']
            filename = save_file(f)
            if filename:
                user.photo = filename
        db.session.commit()
        flash('Profil diperbarui', 'success')
        return redirect(url_for('admin_profile'))
    return render_template('admin/profile.html', form=form, user=user)

# === Skill CRUD ===
@app.route('/admin/skills')
@admin_required
def admin_skills():
    skills = Skill.query.order_by(Skill.id.desc()).all()
    return render_template('admin/skills.html', skills=skills)

@app.route('/admin/skills/new', methods=['GET', 'POST'])
@admin_required
def admin_skill_new():
    form = SkillForm()
    if form.validate_on_submit():
        s = Skill(name=form.name.data, level=form.level.data)
        db.session.add(s)
        db.session.commit()
        flash('Skill ditambahkan', 'success')
        return redirect(url_for('admin_skills'))
    return render_template('admin/edit_skill.html', form=form)

@app.route('/admin/skills/edit/<int:skill_id>', methods=['GET', 'POST'])
@admin_required
def admin_skill_edit(skill_id):
    s = Skill.query.get_or_404(skill_id)
    form = SkillForm(obj=s)
    if form.validate_on_submit():
        s.name = form.name.data
        s.level = form.level.data
        db.session.commit()
        flash('Skill diperbarui', 'success')
        return redirect(url_for('admin_skills'))
    return render_template('admin/edit_skill.html', form=form, skill=s)

@app.route('/admin/skills/delete/<int:skill_id>', methods=['POST'])
@admin_required
def admin_skill_delete(skill_id):
    s = Skill.query.get_or_404(skill_id)
    db.session.delete(s)
    db.session.commit()
    flash('Skill dihapus', 'info')
    return redirect(url_for('admin_skills'))

# === Project CRUD ===
@app.route('/admin/projects')
@admin_required
def admin_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@admin_required
def admin_project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        filename = None
        if 'image' in request.files:
            f = request.files['image']
            filename = save_file(f)
        p = Project(title=form.title.data, description=form.description.data, image=filename, link=form.link.data)
        db.session.add(p)
        db.session.commit()
        flash('Project ditambahkan', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/edit_project.html', form=form)

@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@admin_required
def admin_project_edit(project_id):
    p = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=p)
    if form.validate_on_submit():
        p.title = form.title.data
        p.description = form.description.data
        p.link = form.link.data
        if 'image' in request.files:
            f = request.files['image']
            filename = save_file(f)
            if filename:
                p.image = filename
        db.session.commit()
        flash('Project diperbarui', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/edit_project.html', form=form, project=p)

@app.route('/admin/projects/delete/<int:project_id>', methods=['POST'])
@admin_required
def admin_project_delete(project_id):
    p = Project.query.get_or_404(project_id)
    if p.image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], p.image))
        except Exception:
            pass
    db.session.delete(p)
    db.session.commit()
    flash('Project dihapus', 'info')
    return redirect(url_for('admin_projects'))

if __name__ == "__main__":
    app.run(debug=True)