from user import user

@user.route('/lucy')
def user_lucy():
    return 'user lucy'
@user.route('/tom')
def user_tom():
    return 'user tom'
