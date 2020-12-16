from mainmb.db_models import *
from mainmb import db
from flask_login import login_user
from flask import request, redirect, session
from sqlalchemy import func
from datetime import timedelta
import hashlib


def check_register(name, CMND, username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    u = Hangkhach(HoTen=name, CMND=CMND, tendangnhap=username, password=password)

    try:
        print('running')
        db.session.add(u)
        db.session.commit()
        return True
    except:
        return False


def check_user(Loaiacc=user_role.ADMIN):
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = Hangkhach.query.filter(Hangkhach.tendangnhap == username.strip(),
                                     Hangkhach.password == password,
                                     Hangkhach.Loaiacc == Loaiacc).first()

        if user:
            login_user(user=user)

        if Loaiacc == user_role.ADMIN:
            return redirect('/admin')

        return redirect('/')
    else:
        return redirect('/login')


def get_Sanbay():
    return Sanbay.query.all()


def get_Chuyenbay(SBdi=None, SBden=None, TenCB=None, MaCB=None):
    CBay = db.session.query(Chuyenbay).filter(Chuyenbay.SBdi == SBdi,
                                              Chuyenbay.SBden == SBden).all()
    j = 0
    for i in CBay:
        setattr(i, 'main', ++j)
        setattr(i, 'time_start', str(i.Ngaybay)[11:16])

    return CBay


def conver_str_time(string_time='', time_format="%d-%m-%Y - %H:%M"):
    d = string_time
    return d.strftime(time_format)


def get_SBtrunggian(Ten_Chuyenbay = -1):
    Vao_Sbay = db.session.query(SanBayTrungGian, Sanbay).\
        filter(SanBayTrungGian.MaSB == Sanbay.MaSB).\
        filter(SanBayTrungGian.MaCB == Ten_Chuyenbay).all()

    for i in Vao_Sbay:
        t = i.SanBayTrungGian.GioNghi
        delay = ''
        if t[:2] > '00':
            delay += t[:2] + 'h'
        if t[2:] > '00':
            delay += ' ' + t[2:] + 'm'
        setattr(i.SanBayTrungGian, 'delay', delay)

    return Vao_Sbay


def get_BGia(GiaTien = float):
    Bgia = db.session.query(Bangdongia.GiaTien == GiaTien).all()

    return Bgia