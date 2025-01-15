from dal import DAL
from user_logic import UserLogic

class LikeLogic:
    def __init__(self, dal: DAL,user_logic):
        self.dal = dal
        self.UserLogic = UserLogic


    def _is_valid_user(self, user_id):
      query = self.dal.get_table(
        "SELECT * FROM users WHERE user_id = %s", (user_id,)  
     )
      return len(query) > 0


    def _is_valid_vacation(self, vacation_id):
     query = self.dal.get_table(
        "SELECT * FROM vacations WHERE vacation_id = %s", (vacation_id,)  # Passing vacation_id as a tuple
    )
     return len(query) > 0


    def is_liked(self, user_id, vacation_id):
        query = "SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s"
        results = self.dal.get_table(query, (user_id, vacation_id))
        print(f"Results from is_liked: {results}") 
        return len(results) > 0

    def like_vacation(self, user_id, vacation_id):
      if not self._is_valid_user(user_id) or not self._is_valid_vacation(vacation_id):
        raise ValueError("Invalid user_id or vacation_id.")
    
      if not self.UserLogic.is_regular_user(self, user_id):
        raise ValueError("Only regular users can like vacations.")

      if self.is_liked(user_id, vacation_id):
        return 
    
      query = "INSERT INTO likes (user_id, vacation_id) VALUES (%s, %s)"
      print(f"Executing query: {query} with values ({user_id}, {vacation_id})")
      self.dal._validate_query_params(query, (user_id, vacation_id))  
      self.dal._execute_query(query, (user_id, vacation_id))  
      print(f"✅ Vacation {vacation_id} liked by user {user_id}.")
      return True


    def unlike_vacation(self, user_id, vacation_id):
      if not self._is_valid_user(user_id) or not self._is_valid_vacation(vacation_id):
        raise ValueError("Invalid user_id or vacation_id.")
    
      if not self.UserLogic.is_regular_user(self, user_id):
        raise ValueError("Only regular users can unlike vacations.")

      if not self.is_liked(user_id, vacation_id):
        return 
        
    
      query = "DELETE FROM likes WHERE user_id = %s AND vacation_id = %s"
      self.dal._execute_query(query, (user_id, vacation_id))  
      print(f"✅ Vacation {vacation_id} unliked by user {user_id}.")
      return True
      


    def get_like_count(self, vacation_id):
      query = "SELECT COUNT(*) FROM likes WHERE vacation_id = %s"
      results = self.dal.get_table(query, (vacation_id,))
    
      if results and results[0]['COUNT(*)'] > 0:
        return results[0]['COUNT(*)']
      else:
        print(f"No likes for vacation with ID {vacation_id}.")
        return 0



if __name__ == "__main__":
    dal = DAL()
    like_logic = LikeLogic(dal, UserLogic)

    while True:
      print("\n--- Menu ---")
      print("1. Add Like")
      print("2. View Likes by vacation")
      print("3. Remove Like")
      print("4. Exit")

      choice = input("Select an option (1-4): ")

      if choice == "1":
        print("Entering option 1")  # Debugging
        try:
            user_id = int(input("Enter user_id (integer): "))
            vacation_id = int(input("Enter vacation_id (integer): "))
            print(f"user_id={user_id}, vacation_id={vacation_id}")  # Debugging
            like_logic.like_vacation(user_id, vacation_id)
            print("✅ Like added successfully!")
        except ValueError as e:
            print(f"❌ Value Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

      elif choice == "2":
        try:
            vacation_id = int(input("Enter vacation id (integer): "))
            likes = like_logic.get_like_count(vacation_id)
            print(f"👍 Likes for vacation={vacation_id}: {likes}")
        except ValueError:
            print("❌ Error: Please enter a valid integer!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

      elif choice == "3":
        try:
            user_id = int(input("Enter user_id (integer): "))
            vacation_id = int(input("Enter vacation_id (integer): "))
            like_logic.unlike_vacation(user_id, vacation_id)
            print("✅ Like removed successfully!")
        except ValueError:
            print("❌ Error: Please enter valid integers!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

      elif choice == "4":
        print("Exiting the program. Goodbye!")
        break

      else:
        print("❌ Invalid option. Please select 1, 2, 3, or 4.")
