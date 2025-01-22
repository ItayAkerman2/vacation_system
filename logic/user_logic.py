# src/logic/user_logic.py
from dal import DAL


class UserLogic:
    def __init__(self, dal: DAL):
        self.dal = dal

    def register_user(self, firstname, lastname, email, password, date_of_birth, role_id):
        if len(password) < 6 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            raise ValueError("Password must be at least 6 characters, contain one uppercase letter, and one number.")

        if not self._is_valid_email(email):
            raise ValueError("Invalid email format. It must contain '@' and end with '.com'.")

        query = """
            INSERT INTO users (firstname, lastname, email, password, date_of_birth, role_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.dal.insert(query, (firstname, lastname, email, password, date_of_birth, role_id))
        except Exception as e:
           raise ValueError(f"Error registering user: {e}")



    def _is_valid_email(self, email):
        return '@' in email and email.endswith('.com')
    
    def login_user(self, email, password):
        query = "SELECT * FROM users WHERE email = %s"
        user = self.dal.get_one(query, (email,))
        if user and user['password'] == password:  
            return user
        else:
            raise ValueError("Invalid email or password.")
        
    def is_regular_user(self, user_id):
       query = "SELECT role_id FROM users WHERE user_id = %s"
       result = self.dal.get_table(query, (user_id,))

       print("Result:", result)  
    
       if not result:
          raise ValueError(f"No user found with user_id {user_id}")
    
       return result[0]['role_id'] == 1 

    def is_admin(self, user_id):
        user = self.dal.get_one("SELECT role_id FROM users WHERE user_id = %s", (user_id,))
        return user and user.get("role_id") == 2 
    
    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        try:
            affected_rows = self.dal.delete(query, (user_id,))
            if affected_rows == 0:
                raise ValueError(f"No user found with user_id {user_id}.")
        except Exception as e:
            raise ValueError(f"Error deleting user: {e}")


if __name__ == "__main__":
    dal = DAL()  
    user_logic = UserLogic(dal)
    
    while True:
        print("\n--- Menu ---")
        print("1. Register User")
        print("2. Login User")
        print("3. Check if Regular User")
        print("4. Delete user")
        print("5. Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":  
            firstname = input("Enter first name: ")
            lastname = input("Enter last name: ")
            email = input("Enter email: ")
            password = input("Enter password (at least 6 characters, 1 uppercase letter, 1 number): ")
            date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
            role_id = input("Enter role_id (1 for user, 2 for admin): ")
            
            try:
                role_id = int(role_id)
                user_logic.register_user(firstname, lastname, email, password, date_of_birth, role_id)
                print("User registered successfully.") 
            except ValueError as e:
                print("Error:", e)

                
        
        elif choice == "2":  
            email = input("Enter email: ")
            password = input("Enter password: ")
            
            try:
                logged_in_user = user_logic.login_user(email, password)
                print("User logged in successfully:", logged_in_user)
            except ValueError as e:
                print("Error:", e)

        elif choice == "3":  
            user_id = input("Enter user ID: ")
            try:
                user_id = int(user_id)
                if user_logic.is_regular_user(user_id):
                    print(f"User with ID {user_id} is a regular user.")
                else:
                    print(f"User with ID {user_id} is not a regular user.")
            except ValueError as e:
                print("Error:", e)

        elif choice == "4":
            user_id = input("Enter the user ID to delete: ")
            try:
                user_id = int(user_id)
                user_logic.delete_user(user_id)
                print(f"User with ID {user_id} deleted successfully.")
            except ValueError as e:
                print("Error:", e)

            

        elif choice == "5":  
            print("Exiting the program. Goodbye!")
            break

        else:
            print("❌ Invalid option. Please select 1, 2, 3, or 4.")
