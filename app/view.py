import ast

from werkzeug.security import check_password_hash

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user

from app import app
from app import login_manager
from app.database import UserDatabase
from app.database_manager import get_current_matrix, add, edit_matrix_database, edit_password_database, delete
from app import portal_login


@login_manager.user_loader
def load_user(user_id):
    return UserDatabase.query.get(int(user_id))

@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        add()

        return redirect(url_for('login'))

    explanation = "新しくアカウントを作成します。"
    return render_template("join.html", title='join', explanation=explanation)


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home', user_name=current_user.name))

    if request.method == "POST":
        name = request.form.get('name')
        user = UserDatabase.query.filter_by(name=name).first()

        password = request.form.get('password')

        if not user:
            flash("入力された名前のアカウントが存在しません。")
            return redirect(url_for('login'))

        hashed_password = user.password
        if not check_password_hash(hashed_password, password):
            flash("パスワードが違います。")

            return redirect(url_for('login'))

        else:
            login_user(user)
            return redirect(url_for('home', user_name=user.name))

    explanation = "ユーザー専用ページにログインします。"
    return render_template("login.html", title='login', explanation=explanation)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<string:user_name>')
@login_required
def home(user_name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    title = 'apps'
    return render_template("contents.html", user_name=user_name, title=title, img=False)


@app.route('/user/<string:user_name>/app/login-portal')
@login_required
def login_portal(user_name):
    portal_login.login_portal()
    return redirect(url_for('home', user_name=user_name))


@app.route("/user/<string:user_name>/setting")
@login_required
def setting(user_name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # current_data = get_current_data()
    # columns = create_columns()

    current_matrix = get_current_matrix()
    print(current_matrix)

    return render_template("setting.html", user_name=user_name, current_matrix=current_matrix, title='setting')


@app.route("/user/<string:user_name>/setting/edit-matrix", methods=["POST"])
@login_required
def edit_matrix(user_name):
    edit_matrix_database(user_name)

    return redirect(url_for('setting', user_name=user_name))


@app.route("/user/<string:user_name>/setting/edit-password", methods=["POST"])
@login_required
def edit_password(user_name):
    edit_password_database(user_name)

    return redirect(url_for('setting', user_name=user_name))


@app.route("/setting/delete/<string:obj>", methods=["GET", "DELETE"])
@login_required
def setting_delete(obj):
    which_db_to_delete = request.args.get('which_db_to_delete')
    which_db_to_delete = ast.literal_eval(which_db_to_delete)
    delete(obj, which_db_to_delete)

    return redirect(url_for('setting'))
