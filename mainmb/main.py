from flask import Flask, render_template, request, redirect, url_for, session
# from flask_login import login_user
from mainmb import models
from functools import wraps
from mainmb import mainmb


def login_required(f):
    @wraps(f)
    def check(*args, **kwarg):
        if not session.get("user"):
            return redirect(url_for("login", next=request.url))

        return f(*args, **kwarg)

    return check


@mainmb.route("/")
def main():
    return redirect(url_for("home"))


@mainmb.route("/home", methods=["POST", "GET"])
def home():
    if request.method == ["POST"]:
        return redirect(url_for("register"))
    else:
        return render_template("home.html")


@mainmb.route('/register', methods=['get', 'post'])
def register():
    if session.get("user"):
        return  redirect(request.url)

    err_msg = ""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        if password.strip() != confirm.strip():
            err_msg = "Mật khẩu xác nhận không khớp"
        else:
            if models.add_user(name=name, email=email, username=username, password=password):
                return redirect(url_for("login"))
            else:
                err_msg = "Có gì đó không đúng"

    return render_template('dangki.html', err_msg=err_msg)


@mainmb.route('/login', methods=['GET', 'POST'])
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = models.validate_user(username=username, password=password)
        if user:
            session["user"] = user
            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for("home"))
        else:
            err_msg = "login fail"

    return render_template('login.html', err_msg=err_msg)


@mainmb.route("/logout")
def logout():
    session["user"] = None
    return redirect(url_for("home"))


@mainmb.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    err_msg = ""
    # if request.method == 'POST':

    return render_template('datve.html')


# @login.user_loader
# def get_user(user_id):
#     return utils.get_user_by_id(user_id=user_id)

if __name__ == "__main__":
    # app.secret_key = "^%@&^@*&!@67532623^@%^%@!"
    mainmb.run(debug=True)