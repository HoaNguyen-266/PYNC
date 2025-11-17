from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, User, Book
from forms import LoginForm, BookForm, SignupForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Tên đăng nhập đã tồn tại.')
            return render_template('signup.html', form=form)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký thành công! Hãy đăng nhập.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index.html'))
        flash('Sai tên đăng nhập hoặc mật khẩu')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, description=form.description.data)
        db.session.add(book)
        db.session.commit()
        flash('Thêm sách thành công')
        return redirect(url_for('books'))  
    return render_template('book_form.html', form=form)

@app.route('/books')
@login_required
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)