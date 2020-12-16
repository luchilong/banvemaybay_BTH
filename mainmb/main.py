from flask import render_template, request, url_for, session, jsonify
from mainmb import utils, login
from mainmb import mainmb
from mainmb.decorator import redirect, login_required
from mainmb.admin import db_models, logout_user
from mainmb.db_models import Chuyenbay, Sanbay, Hangkhach, user_role, current_user, db
import json


@mainmb.route("/")
def main():
    f = Chuyenbay.query.all()
    cards = []
    for i in f:
        card ={}
        SB = Sanbay.query.get(i.SBdi)
        card['BayDen'] = SB.TenNuocSB
        card['MaChuyenBay'] = i.MaCB
        card['GioKhoiHanh'] = utils.conver_str_time(i.TGbay)
        card['BatDau'] = Sanbay.query.get(i.SBdi).TenNuocSB
        cards.append(card)

    return render_template("home.html", cards=cards)


@mainmb.route("/home", methods=["post", "get"])
def home():
    if request.method == ["POST"]:
        return redirect(url_for("register"))
    else:
        return render_template("home.html")


@mainmb.route('/register', methods=['get', 'post'])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')

        if password == confirm:
            name = request.form.get('name')
            CMND = request.form.get('CMND')
            username = request.form.get('username')

            if utils.check_register(name=name,
                                    CMND=CMND,
                                    password=password,
                                    username=username):
                return redirect(url_for("login_user"))
            else:
                err_msg = "Có gì đó không đúng"

    return render_template('dangki.html', err_msg=err_msg)


@mainmb.route('/login', methods=['get', 'post'])
def login_user():
    if request.method == 'POST':
        return utils.check_user(Loaiacc=user_role.USER)
    else:
        return render_template('login.html')


@mainmb.route('/login-admin', methods=['post', 'get'])
def login_admin():
    return utils.check_user(Loaiacc=user_role.ADMIN)


@mainmb.route("/logout")
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("home"))


# @mainmb.route('/query', methods=['post', 'get'])
# def quer():
#     return render_template('query.html')


@mainmb.route('/book', methods=['post', 'get'])
@login_required
def book():
    err_msg = ""
    if request.method == 'POST':
        return redirect('/')
    else:
        Sanbays = utils.get_Sanbay()
        return render_template('datve.html', Sanbays=Sanbays)


@mainmb.route('/bookoption', methods=['POST', 'GET'])
def book_option():
    Ve = {}
    Ve['SBdi'] = (request.form.get('SBdi'))
    Ve['SBden'] = (request.form.get('SBden'))
    session['Ve'] = Ve
    SBdi = request.form.get('SBdi')
    SBden = request.form.get('SBden')

    CBay = utils.get_Chuyenbay(SBdi=SBdi,
                               SBden=SBden)

    if len(CBay) == 0:
        mess = "Sorry! We can not found a flight"
        return render_template('datve.html', mess=mess)
    else:
        Vao_SBay = []
        for i in CBay:
            Vao_SBay.append(utils.get_SBtrunggian(Ten_Chuyenbay=i.TenCB))
        if len(Vao_SBay[0]) == 0:
            Vao_SBay = None
        return render_template('bookoption.html', CBay=CBay, Vao_SBay=Vao_SBay)


@mainmb.route('/add_ticket', methods=['post'])
def add_ticket():
    data = json.loads(request.data)
    Ve = session['ve']

    Ve['MaHK'] = current_user.MaHK
    Ve['MaCB'] = data.get("MaCB")
    Ve['MaSB'] = data.get("MaCB")
    Ve['MaPDC'] = data.get("MaPDC")
    Ve['GiaTien'] = data.get("GiaTien")
    session['Ve'] = Ve
    return jsonify({
        "mess": 'Success booking'
    })


@mainmb.route('/payment', methods=['get', 'post'])
def payment():
    GiaTien = request.form.get('GiaTien')
    db_models.Bangdongia(GiaTien=GiaTien)
    if 'Ve' not in session:
        mess="Sorry you not have any ticket"
        return render_template('payment.html', mess=mess)

    if request.method == 'post':
        data = json.loads(request.data)

        payment = data.get("payment")
        position = data.get("position")

        Ve = session['Ve']
        Ve['payment'] = payment
        Ve['position'] = position
        session['Ve'] = Ve

    return render_template('payment.html', Ve=session['Ve'])


@login.user_loader
def get_user(user_id):
    return Hangkhach.query.get(user_id)

if __name__ == "__main__":
    mainmb.run(debug=True)