from app import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(250))
    realname = db.Column(db.String(100))
    avatar = db.Column(db.String(250))

    def __init__(self, username, password, email, realname, avatar):
        self.username = username
        self.password = password
        self.email = email
        self.realname = realname
        self.avatar = avatar


def list_users():
    return User.query.all()


def get_user(id):
    return User.query.get(id)


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def create_user(username, email, password, realname, avatar):
    user = User(username, email, password, realname, avatar)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(id, username=None, email=None, password=None, realname=None,
                avatar=None):
    # This one is harder with the object syntax actually! So we changed the
    # function definition.

    user = User.query.get(id)

    if username:
        user.username = username

    if email:
        user.email = email

    if password:
        user.password = password

    if realname:
        user.realname = realname

    if avatar:
        user.avatar = avatar

    db.session.commit()
    return user


if __name__ == "__main__":
    db.create_all()
