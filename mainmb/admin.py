from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from mainmb import admin, db, db_models
from flask import redirect
from flask_login import current_user, logout_user
from mainmb.db_models import *


class Logout_View(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class db_Model(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_export = True


admin.add_view(db_Model(Sanbay, db.session, name='Sân Bay'))
admin.add_view(db_Model(Chuyenbay, db.session, name='Chuyến bay'))
admin.add_view(db_Model(Hangkhach, db.session, name='Hàng khách'))
admin.add_view(db_Model(Vechuyenbay, db.session, name='Vé'))
admin.add_view(db_Model(SanBayTrungGian, db.session, name='Sân bay trung gian'))
admin.add_view(db_Model(Bangdongia, db.session, name='Bảng đơn giá'))
admin.add_view(db_Model(Chitietchuyenbay, db.session, name='CT Chuyến bay'))
admin.add_view(Logout_View(name='Đăng Xuất'))
