from database import users_collection

class UserModel:
    """
    Entity class that models a user of the app
    @author Andrew Gee
    """

    def __init__(self,email,password,name):
        """
        Creates an instance of a user
        """
        self.email = email
        self.password = password
        self.name = name
    
    def save(self):
        """
        Saves a user to the database
        """
        users_collection.insert_one(self.to_dict())

    def delete(self):
        """
        Deletes a user from the database given their email
        """
        users_collection.delete_one({
            "email":self.email
        })

    def to_dict(self):
        """
        Converts a user instance into dictionary 
        """
        return {
            "email":self.email,
            "password":self.password,
            "name":self.name
        }
    
    @staticmethod
    def find_by_email(email):
        """
        Finds a user from the databse by their email
        """
        data = users_collection.find_one({
            "email":email
        })
        if email:
            return UserModel(data['email'],data['password'],data['name'])
        return None

userModel = UserModel("test@gmail.com","test","Test Test")
user = userModel.find_by_email("test@gmail.com")
if(user is not None):   
    print(user.name)
else:
    print("Could not find user")