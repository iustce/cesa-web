from project.admin import AdminModelView


class PostModelView(AdminModelView):
    column_exclude_list = ('body',)
    column_filters = ('last_modified', 'active', 'importance')
    form_excluded_columns = ('files',)

