from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_user
from mainmb import models


app = Flask(__name__)


@app.route("/")
def main():
    return redirect(url_for("home"))


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == ["POST"]:
        return redirect(url_for("register"))
    else:
        return render_template("home.html")


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password == confirm:
            username = request.form.get('username')
            email = request.form.get('email')

            if utils.add_user(email=email, username=username, password=password):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('dangki.html', err_msg=err_msg)

@app.route('/login', methods=['GET','POST'])
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = models.validate_user(username=username, password=password)
        if user:
            session["user"] = user
            return redirect(url_for("home"))
        else:
            err_msg = "login fail"

    return render_template('login.html', err_msg=err_msg)



@app.route('/book')
def book():
    return render_template('datve.html')


# @login.user_loader
# def get_user(user_id):
#     return utils.get_user_by_id(user_id=user_id)

if __name__ == "__main__":
    app.secret_key = "^%@&^@*&!@67532623^@%^%@!"
    app.run(debug=True)