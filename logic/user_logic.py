from utils.dal import DAL
import re

class UserLogic:
    def __init__(self, dal: DAL):
        self.dal = dal

    def register_user(self, firstname, lastname, email, password, date_of_birth, role_id):
      if len(password) < 6 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        print("❌ Password does not meet requirements.")
        raise ValueError("Password must be at least 6 characters, contain one uppercase letter, and one number.")


      query = """
        INSERT INTO users (firstname, lastname, email, password, date_of_birth, role_id)
        VALUES (%s, %s, %s, %s, %s, %s)
      """
      try:
        self.dal.insert(query, (firstname, lastname, email, password, date_of_birth, role_id))
        print(f"✅ User registered successfully! 🎉")

      except Exception as e:
        print(f"❌ Error during registration: {e}")
        raise ValueError(f"Error registering user: {e}")


    def _is_valid_email(self,email):
     pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
     return re.match(pattern, email) is not None


    def login_user(self, email, password):
        query = "SELECT * FROM users WHERE email = %s"
        user = self.dal.get_one(query, (email,))
        if user and user['password'] == password:  
            return user
        else:
            raise ValueError("Invalid email or password.")

    def delete_user(self, email, password):
      query = "SELECT * FROM users WHERE email = %s"
      user = self.dal.get_one(query, (email,))
    
      if user and user['password'] == password:
        query_delete = "DELETE FROM users WHERE email = %s"
        try:
            affected_rows = self.dal.delete(query_delete, (email,))
            if affected_rows == 0:
                raise ValueError(f"No user found with email {email}.")
            print("✅ User deleted successfully.")
        except Exception as e:
            raise ValueError(f"Error deleting user: {e}")
      else:
        raise ValueError("Invalid email or password.")

if __name__ == "__main__":
    dal = DAL()  
    user_logic = UserLogic(dal)

    while True:
        print("\n--- Menu ---")
        print("1. Register User")
        print("2. Login User")
        print("3. Delete User")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ")

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
                print("✅ User registered successfully.") 
            except ValueError as e:
                print("❌ Error:", e)

        elif choice == "2":  
            email = input("Enter email: ")
            password = input("Enter password: ")

            try:
                logged_in_user = user_logic.login_user(email, password)
                print("✅ Login successful:", logged_in_user)
            except ValueError as e:
                print("❌ Error:", e)

        elif choice == "3":
            user_id = input("Enter the user ID to delete: ")
            try:
                user_id = int(user_id)
                user_logic.delete_user(user_id)
            except ValueError as e:
                print("❌ Error:", e)

        elif choice == "4":  
            print("👋 Exiting the program. Goodbye!")
            break

        else:
            print("❌ Invalid option. Please select 1, 2, 3, or 4.")
