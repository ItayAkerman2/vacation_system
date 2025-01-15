from user_logic import UserLogic
from vacation_logic import VacationLogic
from like_logic import LikeLogic
from unittest.mock import MagicMock


class SystemFacade:
    def __init__(self, dal):
        self.user_logic = UserLogic(dal)
        self.vacation_logic = VacationLogic(dal)
        self.like_logic = LikeLogic(dal, UserLogic)

    def register_user(self, *args):
        self.user_logic.register_user(*args)

    def login_user(self, email, password):
        return self.user_logic.login_user(email, password)

    def create_vacation(self,vacation_title, country_name, start_date, end_date, price, img_url=None):
      self.vacation_logic.create_vacation(vacation_title, country_name, start_date, end_date, price, img_url)

    def update_vacation(self, vacation_id, vacation_title, country_name, start_date, end_date, price, img_url=None):
      self.vacation_logic.update_vacation(vacation_id, vacation_title, country_name, start_date, end_date, price, img_url)

    def get_all_vacations(self):
        return self.vacation_logic.get_all_vacations()

    def like_vacation(self, user_id, vacation_id):
        if self.user_logic.is_regular_user(user_id):
            self.like_logic.like_vacation(user_id, vacation_id)
        else:
            raise PermissionError("Only regular users can like vacations.")

    def unlike_vacation(self, user_id, vacation_id):
        if self.user_logic.is_regular_user(user_id):
            self.like_logic.unlike_vacation(user_id, vacation_id)
        else:
            raise PermissionError("Only regular users can unlike vacations.")


if __name__ == "__main__":
    mock_dal = MagicMock()

    facade = SystemFacade(mock_dal)


    try:
        facade.register_user("John", "Doe", "john@example.com", "securepassword", "1985-03-15", 1)  
        print("register_user: Success")
    except Exception as e:
        print(f"register_user: Failed - {e}")

    mock_dal.get_one.return_value = {"email": "john@example.com", "password": "hashedpassword"}
    try:
        result = facade.login_user("john@example.com", "securepassword")
        print("login_user: Success", result)
    except Exception as e:
        print(f"login_user: Failed - {e}")

    try:
        facade.create_vacation(2, "Vacation to Paris", "Enjoy the Eiffel Tower", "2025-06-01", "2025-06-10", 1000)  
        print("create_vacation: Success")
    except Exception as e:
        print(f"create_vacation: Failed - {e}")

    try:
        facade.update_vacation(2, 101, "Updated Vacation to Paris", "New description", "2025-07-01", "2025-07-10", 1200)  
        print("update_vacation: Success")
    except Exception as e:
        print(f"update_vacation: Failed - {e}")

    mock_dal.get_all.return_value = [
        {"id": 1, "name": "Vacation to Paris"},
        {"id": 2, "name": "Vacation to New York"}
    ]
    try:
        vacations = facade.get_all_vacations()
        print("get_all_vacations: Success", vacations)
    except Exception as e:
        print(f"get_all_vacations: Failed - {e}")

    try:
        facade.like_vacation(1, 101)  
        print("like_vacation: Success")
    except Exception as e:
        print(f"like_vacation: Failed - {e}")

    try:
        facade.unlike_vacation(1, 101)  
        print("unlike_vacation: Success")
    except Exception as e:
        print(f"unlike_vacation: Failed - {e}")
