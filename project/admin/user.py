from project.admin.admin import AdminModelView


class UserModelView(AdminModelView):
    column_exclude_list = ('password', 'tokens')
    form_excluded_columns = ('tokens', 'user_payments', 'courses')
    column_filters = ('name', 'phone', 'national_code', 'student_id')

