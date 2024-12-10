from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User, Job
from . import db

main = Blueprint('main', __name__)

# Mostrar todos los usuarios en home.html
@main.route('/')
def index():
    return render_template('index.html')

# Página de inicio después del login
@main.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html')

# Crear un nuevo usuario (registro)
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        is_company = 'is_company' in request.form  # Verificar si el checkbox está seleccionado

        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.')
            return redirect(url_for('main.register'))

        new_user = User(name=name, email=email, password=password, is_company=is_company)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado exitosamente.')
        return redirect(url_for('main.login'))

    return render_template('register.html')


# Iniciar sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_company'] = user.is_company  # Guardar si el usuario es una empresa
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('main.home'))
        else:
            flash('Email o contraseña incorrectos.')
            return redirect(url_for('main.login'))

    return render_template('login.html')



# Cerrar sesión
@main.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.')
    return redirect(url_for('main.login'))


@main.route('/sobre_nos')
def sobre_nos():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('sobrenos.html')



@main.route('/edit_account', methods=['GET', 'POST'])
def edit_account():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('main.login'))

    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']


        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user and existing_user.id != user.id:
            flash('El email ya está en uso por otro usuario.')
            return redirect(url_for('main.edit_account'))

        user.name = new_name
        user.email = new_email

        db.session.commit()
        session['user_name'] = new_name
        flash('Tu cuenta ha sido actualizada.')
        return redirect(url_for('main.usera'))

    return render_template('edit_account.html', user=user)


@main.route('/usuario')
def usera():
    return render_template('usuario.html')

@main.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente.')
    return redirect(url_for('main.black_father'))




@main.route('/black_father')
def black_father():
    users = User.query.all()
    return render_template('black_father.html', users=users)




@main.route('/trabalhos')
def trabalhos():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))


    jobs = Job.query.all()
    return render_template('trabalhos.html', jobs=jobs)




@main.route('/create-job', methods=['GET', 'POST'])
def create_job():
    if 'user_id' not in session or not session.get('is_company'):
        flash('Debes iniciar sesión como empresa para crear una oferta.')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company_id = session['user_id']

        new_job = Job(title=title, description=description, company_id=company_id)
        db.session.add(new_job)
        db.session.commit()

        flash('Oferta de trabajo creada exitosamente.')
        return redirect(url_for('main.trabalhos'))

    return render_template('create_job.html')






@main.route('/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if 'user_id' not in session or not session.get('is_company'):
        flash('Debes iniciar sesión como empresa para eliminar una oferta.')
        return redirect(url_for('main.login'))

    job = Job.query.get_or_404(job_id)


    if job.company_id != session['user_id']:
        flash('No tienes permiso para eliminar esta oferta.')
        return redirect(url_for('main.trabalhos'))

    db.session.delete(job)
    db.session.commit()
    flash('Oferta de trabajo eliminada exitosamente.')
    return redirect(url_for('main.trabalhos'))




@main.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if 'user_id' not in session or not session.get('is_company'):
        flash('No tienes permiso para acceder a esta página.')
        return redirect(url_for('main.trabalhos'))

    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        db.session.commit()
        flash('La oferta de trabajo ha sido actualizada.')
        return redirect(url_for('main.trabalhos'))

    return render_template('edit_job.html', job=job)




@main.route('/rewin')
def rewin():
    return render_template('reviews.html')