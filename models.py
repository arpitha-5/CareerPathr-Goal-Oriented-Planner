from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.name = user_data.get('name')
        self.bio = user_data.get('bio')
        self.current_role = user_data.get('current_role')
        self.company = user_data.get('company')
        self.linkedin = user_data.get('linkedin')

    def get_id(self):
        return self.id

    def update_profile(self, new_data):
        self.name = new_data.get('name', self.name)
        self.bio = new_data.get('bio', self.bio)
        self.current_role = new_data.get('current_role', self.current_role)
        self.company = new_data.get('company', self.company)
        self.linkedin = new_data.get('linkedin', self.linkedin)
