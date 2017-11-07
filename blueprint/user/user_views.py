from . import user

@user.route('/tom')
def user_tom():
    return 'user tom'
@user.route('/lucy')
def user_lucy():
    return 'user lucy'