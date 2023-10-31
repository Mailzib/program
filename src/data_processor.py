import pandas as pd
from tabulate import tabulate
import re  # Import the regular expression module

# Define the constant CSV file path
CSV_FILE_PATH = '/Users/myouse652/Desktop/Main2.csv'


def search_by_box_number(box_number):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the box number and convert it to a string
        box_number = str(box_number)

        # Iterate through all columns and search for the box number
        found = False
        for column in data.columns:
            result = data[data[column].astype(str) == box_number]
            if not result.empty:
                found = True
                break

        if not found:
            return "Box number not found."

        # Display the result with a title and using tabulate for a table-like format
        result_str = f"Search result for Box number: {box_number}\n"
        result_str += tabulate(result, headers='keys', tablefmt='pretty', showindex=False)

        # Add space lines
        result_str += "\n" * 2

        return result_str

    except Exception as e:
        return str(e)


def search_by_name(name):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the name and convert it to a string
        name = str(name)

        # Create a mask for partial name matching
        mask = data['Name'].str.contains(name, case=False, na=False)

        # Filter the data based on the mask
        result = data[mask]

        if not result.empty:
            # Display the result with a title and using tabulate for a table-like format
            result_str = f"Search result for Name: {name}\n"
            result_str += tabulate(result, headers='keys', tablefmt='pretty', showindex=False)

            # Add space lines
            result_str += "\n" * 2

            return result_str
        else:
            return "Name not found."

    except Exception as e:
        return str(e)


def update_date_by_box_number(box_number, new_date):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the box number and convert it to a string
        box_number = str(box_number)

        # Search for the box number
        found = False
        for column in data.columns:
            result = data[data[column].astype(str) == box_number]
            if not result.empty:
                found = True
                break

        if not found:
            return "Box number not found."

        # Check if the entered new date is valid
        new_date_parsed = pd.to_datetime(new_date, format='%m/%d/%Y', errors='coerce')
        if pd.isna(new_date_parsed):
            return "Invalid date format. Please use 'mm/dd/yyyy'."

        # Format the new date as "mm/dd/yyyy"
        new_date_formatted = new_date_parsed.strftime('%m/%d/%Y')

        # Update the 'Date' column with the new date
        data.loc[result.index, 'Date'] = new_date_formatted
        data.to_csv(CSV_FILE_PATH, index=False,
                    date_format='%m/%d/%Y')  # Save the updated DataFrame to the CSV file with date format
        return f"Date updated for Box number {box_number} to {new_date_formatted}"

    except Exception as e:
        return str(e)


def filter_by_date_and_key(start_date, end_date):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Convert start and end dates to datetime objects
        start_date = pd.to_datetime(start_date, format='%m/%d/%Y')
        end_date = pd.to_datetime(end_date, format='%m/%d/%Y')

        # Convert the 'Date' column to datetime objects
        data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y', errors='coerce')

        # Create a mask to filter dates within the given range
        date_mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)

        # Create a mask to filter rows where 'Got New Key' is 'ok' (case-insensitive)
        key_mask = data['Got New Key'].str.lower() == 'ok'

        # Combine both masks to get the final mask
        result_mask = date_mask & key_mask

        # Filter the data based on the date and 'Got New Key' conditions
        result = data[result_mask]

        if result.empty:
            return "No data found within the specified date range with 'Got New Key' set to 'ok.'"

        # Make a copy of the 'result' DataFrame to avoid the SettingWithCopyWarning
        result = result.copy()

        # Format the 'Date' column to show only the date in the desired format "mm/dd/yyyy"
        result['Date'] = result['Date'].dt.strftime('%m/%d/%Y')

        # Display the result with a title and using tabulate for a table-like format
        result_str = f"Search result for Date Range: {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')} with 'Got New Key' set to 'ok'\n"
        result_str += tabulate(result, headers='keys', tablefmt='pretty', showindex=False)

        # Add space lines
        result_str += "\n" * 2

        return result_str

    except Exception as e:
        return str(e)


# Helper function to add a new row for a box in order

def add_new_box(new_box_data):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the "Box number" and convert it to an integer
        new_box_number = int(new_box_data["Box number"])

        # Check if "Box number" already exists
        if new_box_number in data["Box number"].values:
            # Update the existing row with the new data
            data.loc[data["Box number"] == new_box_number, "Type"] = new_box_data["Type"]
            data.loc[data["Box number"] == new_box_number, "Name"] = new_box_data["Name"]
            data.loc[data["Box number"] == new_box_number, "Date"] = pd.to_datetime(new_box_data["Date"],
                                                                                    format='%m/%d/%Y',
                                                                                    errors='coerce').strftime(
                '%m/%d/%Y')
            data.loc[data["Box number"] == new_box_number, "Phone"] = new_box_data["Phone"]
            data.loc[data["Box number"] == new_box_number, "Got New Key"] = new_box_data["Got New Key"]
            data.loc[data["Box number"] == new_box_number, "Information"] = new_box_data["Information"]
            data.to_csv(CSV_FILE_PATH, index=False,
                        date_format='%m/%d/%Y')  # Save the updated DataFrame to the CSV file with date format
            return f"Box number {new_box_number} has been updated."

        # Find the position to insert the new box number
        existing_box_numbers = data["Box number"].unique()
        existing_box_numbers = [int(box_num) for box_num in existing_box_numbers]
        positions = [i for i, num in enumerate(existing_box_numbers) if num < new_box_number]
        if positions:
            insert_position = max(positions) + 1
        else:
            insert_position = 0

        # Create a new DataFrame for the box
        new_row = pd.DataFrame({
            "Box number": [new_box_number],
            "Type": [new_box_data["Type"]],
            "Name": [new_box_data["Name"]],
            "Date": [pd.to_datetime(new_box_data["Date"], format='%m/%d/%Y', errors='coerce').strftime('%m/%d/%Y')],
            "Phone": [new_box_data["Phone"]],
            "Got New Key": [new_box_data["Got New Key"]],
            "Information": [new_box_data["Information"]]
        })

        # Concatenate the new DataFrame with the existing data
        data = pd.concat([data.iloc[:insert_position], new_row, data.iloc[insert_position:]], ignore_index=True)

        # Sort the DataFrame by "Box number"
        data = data.sort_values(by="Box number").reset_index(drop=True)

        # Save the updated DataFrame to the CSV file
        data.to_csv(CSV_FILE_PATH, index=False, date_format='%m/%d/%Y')

        return f"New box with Box number {new_box_number} has been added."

    except Exception as e:
        return str(e)


def add_name_to_box(box_number, name):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the "Box number" and convert it to an integer
        box_number = int(box_number)

        if box_number not in data["Box number"].values:
            return f"Box number {box_number} does not exist. Please use the 'add_new_box' method to add a new box."

        # Find the position to insert the new box with the given "Box number"
        insert_position = data[data["Box number"] == box_number].index[0] + 1

        # Create a new row with "Box number" and "Name," leaving other columns empty
        new_row = pd.DataFrame({
            "Box number": [box_number],
            "Type": [""],
            "Name": [name],
            "Date": [""],
            "Phone": [""],
            "Got New Key": [""],
            "Information": [""]
        })

        # Concatenate the new row with the existing data at the specified position
        data = pd.concat([data.iloc[:insert_position], new_row, data.iloc[insert_position:]], ignore_index=True)

        # Save the updated DataFrame to the CSV file
        data.to_csv(CSV_FILE_PATH, index=False)

        return f"New row with Box number {box_number} and Name '{name}' has been added."

    except Exception as e:
        return str(e)


def delete_box_by_number(box_number):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Check if the given box number exists in the DataFrame
        if box_number not in data["Box number"].values:
            return f"No boxes with Box number {box_number} found."

        # Delete all rows with the given box number
        data = data[data["Box number"] != box_number]

        # Save the updated DataFrame to the CSV file
        data.to_csv(CSV_FILE_PATH, index=False)

        return f"All boxes with Box number {box_number} have been deleted."

    except Exception as e:
        return str(e)


def display_info_by_status():
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Create a mask to filter rows where 'Got New Key' is 'ok' (case-insensitive)
        key_mask = data['Got New Key'].str.lower() == 'ok'

        # Filter the data based on the 'Got New Key' condition
        filtered_data = data[key_mask]

        if filtered_data.empty:
            return "No data found with 'Got New Key' set to 'ok."

        # Count unique 'Box numbers' in the filtered data
        unique_box_numbers = filtered_data['Box number'].nunique()

        # Count the number of 'Box numbers' for each type (s, m, b) ignoring case
        s_count = filtered_data[filtered_data['Type'].str.lower() == 's']['Box number'].nunique()
        m_count = filtered_data[filtered_data['Type'].str.lower() == 'm']['Box number'].nunique()
        b_count = filtered_data[filtered_data['Type'].str.lower() == 'b']['Box number'].nunique()

        # Display the result with a title and using tabulate for a table-like format
        result_str = "Search result for 'Got New Key' set to 'ok'\n"
        result_str += tabulate(filtered_data, headers='keys', tablefmt='pretty', showindex=False)

        # Add space lines, display the unique 'Box numbers' count, and the counts for each type
        result_str += f"\n\nTotal Box numbers that Got New Keys: {unique_box_numbers}"
        result_str += f"\nTotal Small Boxes: {s_count}"
        result_str += f"\nTotal Medium Boxes: {m_count}"
        result_str += f"\nTotal Big Boxes: {b_count}"

        return result_str

    except Exception as e:
        return str(e)

