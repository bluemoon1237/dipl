

def user_is_student(user):
    return (user.is_authenticated and hasattr(user, 'userprofile')) and not user.userprofile.is_teacher

def user_is_teacher(user):
    return (user.is_authenticated and hasattr(user, 'userprofile')) and user.userprofile.is_teacher
