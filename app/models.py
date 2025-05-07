import base64
from flask_login import UserMixin
from mongoengine import Document, StringField, EmailField, FileField
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    try:
        # More robust user loading by username
        return User.objects(username=user_id).first()
    except Exception as e:
        # Log the error and return None to force re-login
        print(f"Error loading user: {e}")
        return None

class User(Document, UserMixin):
    meta = {'collection': 'users', 'indexes': ['username', 'email']}
    username = StringField(required=True, unique=True, min_length=1, max_length=40)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_pic = FileField()
    
    def get_id(self):
        return self.username
    
    def get_profile_pic(self):
        if not self.profile_pic:
            return None
        try:
            data = self.profile_pic.read()
            encoded = base64.b64encode(data).decode()
            self.profile_pic.close()
            return encoded
        except Exception:
            return None
