import mysql.connector


class DAL:
  
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="127.0.0.1",  

                user="root",   

                password="zxzx2121",     

                database="vacation_system", 
              
                autocommit=True 
            )

        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            self.connection = None

    def _validate_query_params(self, query, params):
      
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if params is not None and not isinstance(params, tuple):
            raise ValueError("Params must be a tuple or None.")

    def _execute_query(self, query, params=None, fetchall=False, fetchone=False):
      
        self._validate_query_params(query, params)
        if self.connection:
            try:
                with self.connection.cursor(dictionary=True) as cursor:
                    print(f"Executing query: {query}")
                    if params:
                        print(f"With parameters: {params}")
                    cursor.execute(query, params)
                    if fetchall:
                        result = cursor.fetchall()
                        print(f"Fetched {len(result)} rows")
                        return result
                    elif fetchone:
                        result = cursor.fetchone()
                        print("Fetched one row")
                        return result
                    else:
                        print(f"Query affected {cursor.rowcount} rows")
                    return cursor
            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
        return None

    def get_table(self, query, params=None):
        return self._execute_query(query, params, fetchall=True)

    def get_scalar(self, query, params=None):
        return self._execute_query(query, params, fetchone=True)

    def insert(self, query, params=None):
        return self._execute_query(query, params)

    def update(self, query, params=None):
        return self._execute_query(query, params)

    def delete(self, query, params=None):
        """מחיקת נתונים מטבלה"""
        return self._execute_query(query, params)

    def get_one(self, query, params=None):
        """שליפת רשומה בודדת"""
        return self._execute_query(query, params, fetchone=True)

    def close(self):
        """סגירת החיבור לבסיס הנתונים"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """
        מתודה זו מופעלת בתחילת בלוק ה-with
        נקראת כאשר נכנסים לבלוק with DAL() as dal
        מחזירה את האובייקט שיוקצה למשתנה אחרי ה-as
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
    

        if self.connection:
            self.close()  # סגירת החיבור לבסיס הנתונים
            print("Connection Closed!")
    
    def _validate_query_params(self, query, params):
      if not isinstance(query, str):
        raise ValueError("Query must be a string.")
      if params is not None and not isinstance(params, (tuple, list)):
        params = (params,)
        return params



# דוגמת שימוש
if __name__ == '__main__':
    with DAL() as dal:
        # דוגמאות ל-get_table
        print("\n=== get_table examples ===")
        countries = dal.get_table("SELECT * FROM countries")
        users = dal.get_table("SELECT * FROM users WHERE age > %s", (25,))

        for country in countries:
            print(f"country name: {country["country_name"]}, id: {
                  country["country_id"]}")

        if users is not None:          
         for user in users:
            print(f"User name:{user['firstname']}, Age:{user["age"]}")

        # # דוגמאות ל-get_scalar
        # print("\n=== get_scalar examples ===")
        # count = dal.get_scalar("SELECT COUNT(*) as count FROM users")
        # max_age = dal.get_scalar("SELECT MAX(age) as max_age FROM users")

        # # דוגמאות ל-get_one
        # print("\n=== get_one examples ===")
        # user = dal.get_one("SELECT * FROM users WHERE id = %s", (1,))
        # country = dal.get_one(
        #     "SELECT * FROM countries WHERE name = %s", ('Israel',))

        # # דוגמאות ל-insert
        # print("\n=== insert examples ===")
        # dal.insert(
        #     "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
        #     ('Johnny1', 'johnny1@example.com', 35)
        # )
        # dal.insert(
        #     "INSERT INTO countries (name, code) VALUES (%s, %s)",
        #     ('Brazil', 'BR')
        # )

        # # דוגמאות ל-update
        # print("\n=== update examples ===")
        # dal.update(
        #     "UPDATE users SET age = %s WHERE id = %s",
        #     (31, 1)
        # )
        # dal.update(
        #     "UPDATE countries SET population = %s WHERE code = %s",
        #     (67000000, 'FR')
        # )

        # # דוגמאות ל-delete
        # print("\n=== delete examples ===")
        # dal.delete(
        #     "DELETE FROM users WHERE id = %s",
        #     (1,)
        # )
        # dal.delete(
        #     "DELETE FROM countries WHERE code = %s",
        #     ('FR',)
        # )