from dal import DAL
from datetime import datetime

class VacationLogic:
    def __init__(self, dal: DAL):
        self.dal = dal

    def create_vacation(self, vacation_title, country_name, start_date, end_date, price, img_url=None):
      
        if not vacation_title or not isinstance(vacation_title, str):
            raise ValueError("Vacation title must be a non-empty string.")
        if len(vacation_title) > 100:  
            raise ValueError("Vacation title must be 100 characters or fewer.")

        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")
        if price < 1000:
            raise ValueError("Price must be between $1,000 and $10,000.")
    
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid start date format: {start_date}. It must be in the format YYYY-MM-DD.")
    
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid end date format: {end_date}. It must be in the format YYYY-MM-DD.")
    
        if start_date_obj <= datetime.now():
            raise ValueError("Start date must be in the future.")
        if end_date_obj <= start_date_obj:
            raise ValueError("End date must be after the start date.")
    
        if not country_name or not isinstance(country_name, str):
            raise ValueError("Country name must be a non-empty string.")
        if len(country_name) > 50:  
            raise ValueError("Country name must be 50 characters or fewer.")

        query = "SELECT country_id FROM countries WHERE country_name = %s"
        result = self.dal.get_table(query, (country_name,))
    
        if not result:
            query = "INSERT INTO countries (country_name) VALUES (%s)"
            self.dal.insert(query, (country_name,))
            result = self.dal.get_table("SELECT country_id FROM countries WHERE country_name = %s", (country_name,))
    
        if not result:
            raise ValueError(f"Failed to get country_id for {country_name}")
    
        country_id = result[0]['country_id']

        query = """
            INSERT INTO vacations (vacation_title, country_id, start_date, end_date, price, img_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.dal.insert(query, (vacation_title, country_id, start_date_obj.strftime('%Y-%m-%d'), end_date_obj.strftime('%Y-%m-%d'), price, img_url))

    def update_vacation(self, vacation_id, vacation_title, country_name, start_date, end_date, price, img_url=None):
        if not isinstance(vacation_id, int):
            raise ValueError("Vacation ID must be an integer.")

        if not vacation_title or not isinstance(vacation_title, str):
            raise ValueError("Vacation title must be a non-empty string.")
        if len(vacation_title) > 100:
            raise ValueError("Vacation title must be 100 characters or fewer.")

        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")
        if price < 1000 :
            raise ValueError("Price must be between $1,000 and $10,000.")
    
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid start date format: {start_date}. It must be in the format YYYY-MM-DD.")
    
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid end date format: {end_date}. It must be in the format YYYY-MM-DD.")
    
        if start_date_obj <= datetime.now():
            raise ValueError("Start date must be in the future.")
        if end_date_obj <= start_date_obj:
            raise ValueError("End date must be after the start date.")
    
        if not country_name or not isinstance(country_name, str):
            raise ValueError("Country name must be a non-empty string.")
        if len(country_name) > 50:
            raise ValueError("Country name must be 50 characters or fewer.")

        query = "SELECT country_id FROM countries WHERE country_name = %s"
        result = self.dal.get_table(query, (country_name,))
    
        if not result:
            query = "INSERT INTO countries (country_name) VALUES (%s)"
            self.dal.insert(query, (country_name,))
            result = self.dal.get_table("SELECT country_id FROM countries WHERE country_name = %s", (country_name,))
    
        if not result:
            raise ValueError(f"Failed to get country_id for {country_name}")
    
        country_id = result[0]['country_id']

        query = """
            UPDATE vacations
            SET vacation_title = %s, country_id = %s, start_date = %s, end_date = %s, price = %s, img_url = %s
            WHERE vacation_id = %s
        """
        self.dal.insert(query, (vacation_title, country_id, start_date_obj.strftime('%Y-%m-%d'), end_date_obj.strftime('%Y-%m-%d'), price, img_url, vacation_id))

    
if __name__ == "__main__":
    dal = DAL()
    vacation_logic = VacationLogic(dal)

    try:
        vacation_logic.create_vacation(
            vacation_title="Beach Paradise",
            country_name="Israel",
            start_date="2025-06-15",
            end_date="2025-06-22",
            price=3000,
            img_url="http://example.com/beach.jpg"
        )
        print("Vacation created successfully.")
        
        vacation_logic.update_vacation(
            vacation_id=1,
            vacation_title="Updated Beach Paradise",
            country_name="Israel",
            start_date="2025-07-01",
            end_date="2025-07-10",
            price=3500,
            img_url="http://example.com/updated_beach.jpg"
        )
        print("Vacation updated successfully.")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")