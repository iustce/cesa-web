# flask imports
from flask import request, url_for, redirect
from flask.ext.admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin


class AdminModelView(ModelView):
    can_view_details = True
    can_export = True
    details_modal = True

    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class AdminFile(FileAdmin):
    def is_accessible(self):
        return True
