from shop import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return Admin.query.get(user_id)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    admin = db.Column(db.Boolean, default=True)
    moderator = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Użytkownik: {self.username}'


db.create_all()