from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from main import admin



class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


admin.add_view(ContactView(name='Liên hệ'))
