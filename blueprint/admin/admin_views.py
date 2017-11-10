from . import admin

@admin.route('/jerry/')
def admin_jerry():
    return 'admin jerry'
@admin.route('/jack/')
def admin_jack():
    return 'admin jack'
