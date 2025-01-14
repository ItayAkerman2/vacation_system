from facade import SystemFacade
from dal import DAL
from datetime import datetime

def main():
    dal = DAL()
    system_facade = SystemFacade(dal)

    user = None  

    while True:
        print("\n✨===== Welcome to the Vacation System =====✨")
        print("🌟 1. Register (👤)")
        print("🔑 2. Login (🔓)")
        print("🏝️ 3. Add Vacation (✈️)")
        print("💼 4. Update Vacation (✏️)")
        print("❤️ 5. Add Like (👍)")
        print("🚪 6. Exit (👋)")
        choice = input("➡️ Choose an option: ").strip()

        if choice == "1":
            
            print("\n👤 --- Register New User ---")
            try:
                first_name = input("📝 Enter First Name: ").strip()
                last_name = input("📝 Enter Last Name: ").strip()
                email = input("📧 Enter Email: ").strip()
                password = input("🔑 Enter Password: ").strip()
                date_of_birth = input("📅 Enter Date of Birth (DD-MM-YYYY): ").strip()

                print("\n🎭 Role Options:")
                print("1 - 👤 User")
                print("2 - 👑 Admin")
                role_input = input("➡️ Enter Role (1 for User, 2 for Admin): ").strip()

                if role_input == "1":
                    role_id = 1  
                elif role_input == "2":
                    role_id = 2  
                else:
                    print("❌ Error: Invalid Role! Please choose 1 (User) or 2 (Admin).")
                    continue

                user_id = system_facade.register_user(first_name, last_name, email, password, date_of_birth, role_id)
                print(f"✅ User registered successfully! 🎉 Your User ID is: {user_id}")
            except Exception as e:
                print(f"❌ Error during registration: {e}")

        elif choice == "2":
            
            print("\n🔓 --- User Login ---")
            try:
                email = input("📧 Enter Email: ").strip()
                password = input("🔑 Enter Password: ").strip()
                user = system_facade.login_user(email, password)

                print(f"✅ Welcome, {user['firstname']} {user['lastname']}! 🎊")
                print(f"🆔 Your User ID is: {user['user_id']}")
            except Exception as e:
                print(f"❌ Error during login: {e}")

        elif choice == "3":
            if user and user['role_id'] == 2: 
                print("\n🏝️ --- Add Vacation ---")
                try:
                    vacation_title = input("✏️ Enter Vacation Title: ").strip()
                    vacation_start_date = input("📅 Enter Vacation Start Date (DD-MM-YYYY): ").strip()
                    vacation_end_date = input("📅 Enter Vacation End Date (DD-MM-YYYY): ").strip()
                    price = float(input("💲 Enter Vacation Price: ").strip())
                    img_url = input("🖼️ Enter Image URL (optional): ").strip() or None

                    vacation_start_date_obj = datetime.strptime(vacation_start_date, "%d-%m-%Y")
                    vacation_end_date_obj = datetime.strptime(vacation_end_date, "%d-%m-%Y")

                    system_facade.create_vacation(vacation_title, vacation_start_date_obj, vacation_end_date_obj, price, img_url)
                    print("✅ Vacation added successfully!")
                except Exception as e:
                    print(f"❌ Error during adding vacation: {e}")
            else:
                print("❌ Only admins can add vacations.")

        elif choice == "4":
            if user and user['role_id'] == 2:  
                print("\n💼 --- Update Vacation ---")
                try:
                    vacation_id = int(input("🏝️ Enter Vacation ID: ").strip())
                    new_vacation_title = input("✏️ Enter New Vacation Title: ").strip()
                    new_vacation_start_date = input("📅 Enter New Start Date (DD-MM-YYYY): ").strip()
                    new_vacation_end_date = input("📅 Enter New End Date (DD-MM-YYYY): ").strip()
                    new_price = float(input("💲 Enter New Price: ").strip())
                    new_img_url = input("🖼️ Enter New Image URL (optional): ").strip() or None

                    # עדכון תאריך בפורמט ישראלי
                    new_start_date_obj = datetime.strptime(new_vacation_start_date, "%d-%m-%Y")
                    new_end_date_obj = datetime.strptime(new_vacation_end_date, "%d-%m-%Y")

                    system_facade.update_vacation(vacation_id, new_vacation_title, new_start_date_obj, new_end_date_obj, new_price, new_img_url)
                    print("✅ Vacation updated successfully!")
                except Exception as e:
                    print(f"❌ Error during updating vacation: {e}")
            else:
                print("❌ Only admins can update vacations.")

        elif choice == "5":
            # הוספת לייק
            print("\n❤️ --- Add Like ---")
            try:
                user_id = int(input("🆔 Enter Your User ID: ").strip())
                vacation_id = int(input("🏝️ Enter Vacation ID: ").strip())
                system_facade.like_vacation(user_id, vacation_id)
                print("👍 Like added successfully!")
            except Exception as e:
                print(f"❌ Error during adding like: {e}")

        elif choice == "6":
            # יציאה
            print("👋 Goodbye! See you next time.")
            break

        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
