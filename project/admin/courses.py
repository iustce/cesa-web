from project.admin.admin import AdminModelView


class CourseModelView(AdminModelView):
    column_exclude_list = ('body',)
    form_excluded_columns = ('payment', )
    column_filters = ('start_date', 'end_date', 'price')

