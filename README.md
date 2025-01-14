
# Python Vacation System Project

## **Project Overview**
This project implements a **Vacation Management System** using **Python** and **MySQL**, following a **three-layer architecture**:
1. **Data Access Layer (DAL)** for database operations.
2. **Business Logic Layer (Logic)** for validations and business rules.
3. **Facade Layer** for a simple and intuitive interface.

### **Key Details**
- **Course**: Python
- **Team Size**: Pairs (2 students)
- **Duration**: 3 weeks
- **Database**: MySQL
- **Architecture**: Object-Oriented Programming (OOP)

---

## **Features**

### **User Features**
1. Register a new account.
2. Login/Logout.
3. View all available vacations.
4. Like/unlike vacations.
5. View liked vacations.

### **Admin Features**
1. Add new vacations.
2. Edit existing vacations.
3. Delete vacations.
4. Admins cannot like/unlike vacations.

---

## **System Architecture**

### **1. Data Access Layer (DAL)**
Located in `utils/dal.py`. Handles:
- Database connections.
- All SQL queries (SELECT, INSERT, UPDATE, DELETE).
- No business logic included.

### **2. Business Logic Layer**
Located in `logic/`. Handles:
- Validations (e.g., password rules, date constraints).
- Implementation of business rules.
- No direct database access.
  
Submodules:
- `user_logic.py` – Manages users.
- `vacation_logic.py` – Manages vacations.
- `like_logic.py` – Manages likes.

### **3. Facade Layer**
Located in `facade/system_facade.py`. Provides:
- A unified interface for operations.
- Coordinates between Logic and DAL layers.
- No business logic or database queries.

---

## **Database Structure**

### **Tables**
1. **Users**
   - `user_id` (PK)
   - `firstname` (required)
   - `lastname` (required)
   - `email` (unique, required)
   - `password` (hashed, minimum 6 characters, 1 uppercase letter, 1 number)
   - `date_of_birth` (required)
   - `role_id` (FK to Roles)

2. **Vacations**
   - `vacation_id` (PK)
   - `vacation_title` (required)
   - `country_id` (FK to Countries)
   - `start_date` (must be in the future)
   - `end_date` (must be after start date)
   - `price` (minimum: $1,000; maximum: $10,000)
   - `total_likes`
   - `img_url` (optional)

3. **Roles**
   - `role_id` (PK)
   - `role_name` (`user` or `admin`)

4. **Likes**
   - `like_id` (PK)
   - `vacation_id` (FK)
   - `user_id` (FK)
   - Each user can like each vacation only once.

5. **Countries**
   - `country_id` (PK)
   - `country_name`

---

## **Project Structure**

```plaintext
vacation-system/
├── src/
│   ├── utils/
│   │   └── dal.py
│   ├── logic/
│   │   ├── user_logic.py
│   │   ├── vacation_logic.py
│   │   └── like_logic.py
│   ├── facade/
│   │   └── system_facade.py
│   └── main.py
├── requirements.txt
└── README.md
```

---


### **4. Run the Application**
Each file in the project contains a section for running and testing its functions directly using `if __name__ == "__main__":`.  
You can run these files to test specific features:
```bash
python src/utils/dal.py
python src/logic/user_logic.py
python src/logic/vacation_logic.py
python src/logic/like_logic.py
python src/facade/system_facade.py
python src/main.py
```

---

## **Important Notes**
1. Follow OOP principles.
2. Ensure that all database tables have the required structure and data.
3. Keep the repository up to date on GitHub.

---
