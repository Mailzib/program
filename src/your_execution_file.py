from src.data_processor import (
    search_by_box_number, search_by_name, update_date_by_box_number,
    filter_by_date_and_key, add_new_box, add_name_to_box,
    delete_box_by_number, delete_row_by_name, display_info_by_status_as_pdf, back_up,
    update_box_by_number, move_rows, add_entry_to_accounting, back_up_accounting
)


def execute_methods():
    while True:
        print("+++++++++++++++++++++     Mail ZIB Program Starting    +++++++++++++++++++")
        print("Choose a method to execute:")
        print("1. Search by box number")
        print("2. Search by name")
        print("3. Renew ")
        print("4. Filter by dates to see renew list - PDF")
        print("5. Open new Box")
        print("6. Add extra name for an existing box")
        print("7. Delete a box by number")
        print("8. Delete Extra Name")
        print("9. Update Information for existing box")
        print("10.Back up and get active Box list- PDF")
        print("11. Add entry to accounting")
        print("0. Quit")

        choice = input("Enter the number of the method you want to execute (0 to quit): ")

        if choice == '1':
            box_number = input("Enter the box number: ")
            try:
                box_number = int(box_number)
                if 101 <= box_number <= 550:
                    result = search_by_box_number(box_number)
                else:
                    result = "Box number must be between 101 and 550."
            except ValueError:
                result = "Invalid input for box number."
        elif choice == '2':
            name = input("Enter the name (Part of name can enter): ")
            result = search_by_name(name)
        elif choice == '3':
            result = move_rows()
            box_number = input("Enter the box number: ")
            months_to_add = input("Enter the number of months to add: ")
            payment_method = input("Enter the Payment Method: ")
            representative_name = input("Enter the Mailzib representative name: ")
            try:
                box_number = int(box_number)
                months_to_add = int(months_to_add)
                result = update_date_by_box_number(box_number, months_to_add, representative_name, payment_method)
            except ValueError:
                result = "Invalid input for box number or number of months."
        elif choice == '4':
            start_date = input("Enter the start date (mm/dd/yyyy): ")
            end_date = input("Enter the end date (mm/dd/yyyy): ")
            result = filter_by_date_and_key(start_date, end_date)
        elif choice == '5':
            new_box_data = {}
            new_box_data["Box number"] = int(input("Enter the box number: "))
            new_box_data["Name"] = input("Enter the name: ")
            new_box_data["Date"] = input("Enter the date (mm/dd/yyyy): ")
            new_box_data["Phone"] = input("Enter the phone number: ")
            new_box_data["Did get new key?"] = input("Did get a new key? (Y/N): ")
            new_box_data["Information"] = input("Enter additional information: ")
            result = add_new_box(new_box_data)
        elif choice == '6':
            box_number = int(input("Enter the box number: "))
            name = input("Enter the name to add: ")
            add_phone = input("Do you want to add a phone number (Y/N)? ").strip().lower()
            if add_phone == 'y':
                phone = input("Enter the phone number to add: ")
                result = add_name_to_box(box_number, name, phone)
            else:
                result = add_name_to_box(box_number, name)
        elif choice == '7':
            box_number = input("Enter the box number to delete: ")
            result = delete_box_by_number(int(box_number))
        elif choice == '8':
            result = delete_row_by_name()
        elif choice == '9':
            box_number = int(input("Enter the box number: "))
            result = update_box_by_number(box_number)
        elif choice == '10':
            result = move_rows()
            result = display_info_by_status_as_pdf()
            result += "\n" + back_up()
            result += "\n" + back_up_accounting()
        elif choice == '11':
            result = add_entry_to_accounting()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        print("---------------------------------- Result -----------------------------------------------------")
        print(result)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^- Program Ending ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("\n" * 1)


if __name__ == "__main__":
    execute_methods()
