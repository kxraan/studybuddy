import base64
import bson
import io
from flask_login import UserMixin
from bson.objectid import ObjectId
from . import login_manager, mongo
from werkzeug.utils import secure_filename
import os

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.password = user_data.get('password')
        self._id = user_data.get('_id')
        self.profile_pic = user_data.get('profile_pic')
    
    def get_id(self):
        return self.username
    
    def get_profile_pic(self):
        """Get the profile picture as a base64 encoded string for display in HTML"""
        if not self.profile_pic:
            return None
        try:
            # If the profile pic is stored as binary data in MongoDB
            if isinstance(self.profile_pic, bytes) or isinstance(self.profile_pic, bson.binary.Binary):
                return base64.b64encode(self.profile_pic).decode('utf-8')
            # If it's stored as a base64 string already
            elif isinstance(self.profile_pic, str):
                return self.profile_pic
            return None
        except Exception as e:
            print(f"Error getting profile picture: {e}")
            return None
    
    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        return User(user_data) if user_data else None
    
    @staticmethod
    def get_by_email(email):
        user_data = mongo.db.users.find_one({"email": email})
        return User(user_data) if user_data else None
    
    def save_profile_pic(self, image_file):
        """Save a profile picture to MongoDB"""
        try:
            # Read the image data
            image_binary = image_file.read()
            
            # Update the user document with the image binary data
            mongo.db.users.update_one(
                {"username": self.username},
                {"$set": {"profile_pic": image_binary}}
            )
            
            # Update the local instance
            self.profile_pic = image_binary
            return True
        except Exception as e:
            print(f"Error saving profile picture: {e}")
            return False

@login_manager.user_loader
def load_user(username):
    try:
        # Load user by username
        user_data = mongo.db.users.find_one({"username": username})
        if not user_data:
            return None
        return User(user_data)
    except Exception as e:
        print(f"Error loading user: {e}")
        return None
