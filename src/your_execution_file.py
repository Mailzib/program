from src.data_processor import (
    search_by_box_number, search_by_name, update_date_by_box_number,
    filter_by_date_and_key, add_new_box, add_name_to_box,
    delete_box_by_number, display_info_by_status
)


def execute_methods():
    while True:
        print("+++++++++++++++++++++     Mail ZIB Program Starting    +++++++++++++++++++")
        print("Choose a method to execute:")
        print("1. Search by box number")
        print("2. Search by name")
        print("3. Renew - Update the date for a specific box number")
        print("4. Filter by dates")
        print("5. Add a new box or update the existing Box")
        print("6. Add a name to a box - extra name for an existing box")
        print("7. Delete a box by number")
        print("8. Display how many active customers do we have")
        print("0. Quit")

        choice = input("Enter the number of the method you want to execute (0 to quit): ")

        if choice == '1':
            box_number = input("Enter the box number: ")
            box_number = int(box_number)
            if 101 <= box_number <= 550:
                result = search_by_box_number(box_number)
            else:
                result = "Box number must be between 101 and 550."
        elif choice == '2':
            name = input("Enter the name (partial match): ")
            result = search_by_name(name)
        elif choice == '3':
            box_number = input("Enter the box number: ")
            new_date = input("Enter the new date (mm/dd/yyyy): ")
            result = update_date_by_box_number(int(box_number), new_date)
        elif choice == '4':
            start_date = input("Enter the start date (mm/dd/yyyy): ")
            end_date = input("Enter the end date (mm/dd/yyyy): ")
            result = filter_by_date_and_key(start_date, end_date)
        elif choice == '5':
            new_box_data = {
                "Box number": input("Box number: "),
                "Type": input("Type: "),
                "Name": input("Name: "),
                "Date": input("Date (mm/dd/yyyy): "),
                "Phone": input("Phone: "),
                "Got New Key": input("Got New Key: "),
                "Information": input("Information: "),
            }
            box_number = int(new_box_data["Box number"])
            if 101 <= box_number <= 550:
                result = add_new_box(new_box_data)
            else:
                result = "Box number must be between 101 and 550."
        elif choice == '6':
            box_number = input("Enter the box number: ")
            name = input("Enter the name to add: ")
            result = add_name_to_box(int(box_number), name)
        elif choice == '7':
            box_number = input("Enter the box number to delete: ")
            result = delete_box_by_number(int(box_number))
        elif choice == '8':
            result = display_info_by_status()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        print("---------------------------------- Result -----------------------------------------------------")
        print("\n" * 1)
        print(result)
        print("\n" * 1)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^- Program Ending ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("\n" * 1)


if __name__ == "__main__":
    execute_methods()




