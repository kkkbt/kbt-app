from werkzeug.security import generate_password_hash

from flask import request
from flask_login import current_user

from app import db
from app.database import UserDatabase, PortalDatabase





def get_stored_matrix():
    user = PortalDatabase.query.filter_by(name=current_user.name).first()

    return {
        "A": user.matrix_A,
        "B": user.matrix_B,
        "C": user.matrix_C,
        "D": user.matrix_D,
        "E": user.matrix_E,
        "F": user.matrix_F,
        "G": user.matrix_G,
        "H": user.matrix_H,
        "I": user.matrix_I,
        "J": user.matrix_J
    }


def get_stored_portal_password():
    user = PortalDatabase.query.filter_by(name=current_user.name).first()

    return {
        "student_number": user.student_number,
        "portal_password": user.portal_password
    }


def get_current_matrix():
    stored_matrix = get_stored_matrix()

    current_matrix = {}
    for char in stored_matrix:
        if stored_matrix[char]:
            if len(stored_matrix[char]) == 13:
                current_matrix[char] = [stored_matrix[char][2 * i] for i in range(7)]
            else:
                current_matrix[char] = ["" for _ in range(7)]
        else:
            current_matrix[char] = ["" for _ in range(7)]
    return current_matrix


def add():
    name = request.form["name"]
    password = request.form.get("password")
    email = request.form.get("password_confirmation")

    password = generate_password_hash(password)
    email = generate_password_hash(email)

    db.session.add(UserDatabase(
        name=name,
        email=email,
        password=password
    ))
    db.session.add(PortalDatabase(
        name=name
    ))

    db.session.commit()

    return


def edit_matrix_database(user_name):
    user = PortalDatabase.query.filter_by(name=user_name).first()
    current_matrix = {}

    for char in "ABCDEFGHIJ":
        tmp_list = []
        for i in range(7):
            tmp_list.append(request.form.get(f'{char}{i}').upper())
        x = " ".join(tmp_list)
        current_matrix[char] = x

    user.matrix_A = current_matrix["A"]
    user.matrix_B = current_matrix["B"]
    user.matrix_C = current_matrix["C"]
    user.matrix_D = current_matrix["D"]
    user.matrix_E = current_matrix["E"]
    user.matrix_F = current_matrix["F"]
    user.matrix_G = current_matrix["G"]
    user.matrix_H = current_matrix["H"]
    user.matrix_I = current_matrix["I"]
    user.matrix_J = current_matrix["J"]
    db.session.commit()
    return

def edit_password_database(user_name):
    user = PortalDatabase.query.filter_by(name=user_name).first()

    user.student_number = request.form.get("student_number")
    user.portal_password = request.form.get("portal_password")

    db.session.commit()
    return


def delete(obj, which_db_to_delete):
    pass
