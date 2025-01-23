from facade.facade import SystemFacade
from utils.dal import DAL
from datetime import datetime

def main():
    dal = DAL()
    system_facade = SystemFacade(dal)

    user = None  

    while True:
        print("\n🌟✨===== Welcome to the Vacation System =====✨🌟")
        print("👤 1. Register")
        print("🔑 2. Login")
        print("🚪 3. Exit")
        choice = input("➡️ Choose an option: ").strip()

        if choice == "1":
            print("\n👤 --- Register New User ---")
            try:
                first_name = input("📝 Enter First Name: ").strip()
                last_name = input("📝 Enter Last Name: ").strip()
                email = input("📧 Enter Email: ").strip()
                if not system_facade._is_valid_email(email):
                   print("❌ Invalid email format. It must contain '@' and end with '.com'.")
                   continue
                password = input("🔑 Enter Password (min 6 characters, 1 uppercase, 1 number): ").strip()
                if len(password) < 6 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
                   print("❌ Password must be at least 6 characters, contain one uppercase letter, and one number.")
                   continue
                date_of_birth = input("📅 Enter Date of Birth (YYYY-MM-DD): ").strip()
                role_id = 1  
                
                system_facade.register_user(first_name, last_name, email, password, date_of_birth, role_id)
               
                
            except Exception as e:
                print(f"❌ Error during registration: {e}")

        elif choice == "2":
            print("\n🔑 --- User Login ---")
            try:
                email = input("📧 Enter Email: ").strip()
                password = input("🔑 Enter Password: ").strip()
                user = system_facade.login_user(email, password)

                print(f"✅ Welcome, {user['firstname']} {user['lastname']}! 🎊")
                print(f"🆔 Your User ID: {user['user_id']}")

                
                if user['role_id'] == 1: 
                    user_menu(user, system_facade)
                elif user['role_id'] == 2: 
                    admin_menu(user, system_facade)
            except Exception as e:
                print(f"❌ Login failed: {e}")

        elif choice == "3":
            print("👋 Goodbye! See you next time.")
            break

        else:
            print("❌ Invalid choice! Please try again.")

def user_menu(user, system_facade):
    while True:
        print("\n🌟 --- User Menu --- 🌟")
        print("❤️ 1. Add Like")
        print("👎 2. Remove Like")
        print("🏝️ 3. View Vacations")
        print("🗑️ 4. Delete Account")
        print("🚪 5. Logout")
        choice = input("➡️ Choose an option: ").strip()

        if choice == "1":
            print("\n❤️ --- Add Like ---")
            try:
                system_facade.show_all_vacations_with_likes()
                vacation_id = int(input("🏝️ Enter Vacation ID: ").strip())
                system_facade.like_vacation(user['user_id'], vacation_id)
            except Exception as e:
                print(f"❌ Error during adding like: {e}")

        elif choice == "2":
            print("\n👎 --- Remove Like ---")
            try:
                system_facade.show_all_vacations_with_likes()
                vacation_id = int(input("🏝️ Enter Vacation ID: ").strip())
                system_facade.unlike_vacation(user['user_id'], vacation_id)
            except Exception as e:
                print(f"❌ Error during removing like: {e}")

        elif choice == "3":
            print("\n🏝️ --- View Vacations ---")
            try:
                system_facade.show_all_vacations_with_likes()
            except Exception as e:
                print(f"❌ Error displaying vacations: {e}")

        elif choice == "4":
            print("\n🗑️ --- Delete Account ---")
            confirmation = input("⚠️ Are you sure you want to delete your account? (yes/no): ").strip().lower()
            
            if confirmation == 'yes':
                try:
                    email = input("📧 Enter your email: ").strip()
                    password = input("🔑 Enter your password: ").strip()

                    system_facade.delete_user(email,password)
                    print("✅ Account deleted successfully.")
                    break
                except Exception as e:
                    print(f"❌ Error during account deletion: {e}")
            else:
                print("❌ Account deletion cancelled.")

        elif choice == "5":
            print("👋 Logging out...")
            break

        else:
            print("❌ Invalid choice! Please try again.")


def admin_menu(user, system_facade):
    while True:
        print("\n👑 --- Admin Menu --- 👑")
        print("✈️ 1. Add Vacation")
        print("🛠️ 2. Update Vacation")
        print("🗑️ 3. Delete Vacation")
        print("🚪 4. Logout")
        choice = input("➡️ Choose an option: ").strip()

        if choice == "1":
            print("\n✈️ --- Add Vacation ---")
            try:
                title = input("✏️ Enter Vacation Title: ").strip()
                start_date = input("📅 Enter Start Date (YYYY-MM-DD): ").strip()
                end_date = input("📅 Enter End Date (YYYY-MM-DD): ").strip()
                country = input("🌍 Enter Country: ").strip()
                price = float(input("💲 Enter Price: ").strip())
                img_url = input("🖼️ Enter Image URL (optional): ").strip() or None

                system_facade.create_vacation(title, country, start_date, end_date, price, img_url)
                print("✅ Vacation added successfully!")
            except Exception as e:
                print(f"❌ Error during adding vacation: {e}")

        elif choice == "2":
            print("\n🛠️ --- Update Vacation ---")
            try:
                system_facade.show_all_vacations_with_likes()
                vacation_id = int(input("🏝️ Enter Vacation ID to Update: ").strip())
                
                vacation_exists = system_facade.get_vacation_by_id(vacation_id)
                if vacation_exists:
                    print("❌ The vacation ID does not exist!")
                    continue
                
                title = input("✏️ Enter New Title: ").strip()
                start_date = input("📅 Enter New Start Date (YYYY-MM-DD): ").strip()
                end_date = input("📅 Enter New End Date (YYYY-MM-DD): ").strip()
                country = input("🌍 Enter New Country: ").strip()
                price = float(input("💲 Enter New Price: ").strip())
                img_url = input("🖼️ Enter New Image URL (optional): ").strip() or None

                system_facade.update_vacation(vacation_id, title, country, start_date, end_date, price, img_url)
                print("✅ Vacation updated successfully!")
            except Exception as e:
                print(f"❌ Error during updating vacation: {e}")

        elif choice == "3":
            print("\n🗑️ --- Delete Vacation ---")
            try:
                system_facade.show_all_vacations_with_likes()
                vacation_id = int(input("🏝️ Enter Vacation ID to Delete: ").strip())
                
                vacation_exists = system_facade.get_vacation_by_id(vacation_id)
                if vacation_exists:
                    print("❌ The vacation ID does not exist!")
                    continue

                system_facade.delete_vacation(vacation_id)
                print("✅ Vacation deleted successfully!")
            except Exception as e:
                print(f"❌ Error during deleting vacation: {e}")

        elif choice == "4":
            print("👋 Logging out...")
            break

        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
