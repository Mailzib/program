import datetime
import warnings

import pandas as pd
import os
from reportlab.lib.styles import getSampleStyleSheet
from tabulate import tabulate
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime, timedelta
from reportlab.lib import colors, styles
from dateutil.relativedelta import relativedelta

CSV_FILE_PATH = 'F:/Data Base/MainDBNOV4.csv'
ACCOUNTING_FILE_PATH = "F:/Data Base/accounting.csv"
S_1_month_Price = 30
S_3_month_Price = 72 / 3
S_6_month_Price = 130 / 6
S_12_month_Price = 240 / 12

M_1_month_Price = 45
M_3_month_Price = 100 / 3
M_6_month_Price = 175 / 6
M_12_month_Price = 330 / 12

B_1_month_Price = 56
B_3_month_Price = 130 / 3
B_6_month_Price = 216 / 6
B_12_month_Price = 410 / 12


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


def update_date_by_box_number(box_number, months_to_add, representative_name, payment_method):
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

        # Get the existing date for the box
        existing_date = result.loc[result.index[0], 'Date']

        # Check if the existing date is not 'nan'
        if pd.notna(existing_date):
            existing_date = datetime.strptime(str(existing_date), '%m/%d/%Y')
        else:
            return "Existing date is not available or is not in the expected format."

        # Initialize free_months with a default value
        free_months = 0

        # Ask the user if they want to add some months as free charge as a discount
        add_free_months = input("Do you want to add some months as a free charge as a discount? (Y/N): ").upper()

        if add_free_months == 'Y':
            # Ask the user for the number of free months
            free_months = int(input("Enter the number of free months to add: "))
            new_date = existing_date + relativedelta(months=months_to_add + free_months)
        else:
            # Calculate the new date by adding the specified number of months
            new_date = existing_date + relativedelta(months=months_to_add)

        # Update the DataFrame with the new date
        data.loc[result.index[0], 'Date'] = new_date.strftime('%m/%d/%Y')

        # Save the updated DataFrame back to the CSV file
        data.to_csv(CSV_FILE_PATH, index=False)

        # Calculate the price based on the given conditions
        type_code = result.loc[result.index[0], 'Type'].lower()
        price_per_month = 0

        size_display = ""
        if type_code == 's':
            # ... (your existing price calculation logic)
            size_display = "Small"
        elif type_code == 'm':
            # ... (your existing price calculation logic)
            size_display = "Medium"
        elif type_code == 'b':
            # ... (your existing price calculation logic)
            size_display = "Big"

        if type_code == 's':
            if 1 <= months_to_add < 3:
                price_per_month = S_1_month_Price
            elif 3 <= months_to_add < 6:
                price_per_month = S_3_month_Price
            elif 6 <= months_to_add < 12:
                price_per_month = S_6_month_Price
            elif months_to_add == 12:
                price_per_month = S_12_month_Price
        elif type_code == 'm':
            if 1 <= months_to_add < 3:
                price_per_month = M_1_month_Price
            elif 3 <= months_to_add < 6:
                price_per_month = M_3_month_Price
            elif 6 <= months_to_add < 12:
                price_per_month = M_6_month_Price
            elif months_to_add == 12:
                price_per_month = M_12_month_Price
        elif type_code == 'b':
            if 1 <= months_to_add < 3:
                price_per_month = B_1_month_Price
            elif 3 <= months_to_add < 6:
                price_per_month = B_3_month_Price
            elif 6 <= months_to_add < 12:
                price_per_month = B_6_month_Price
            elif months_to_add == 12:
                price_per_month = B_12_month_Price

        price = round(price_per_month * months_to_add)

        # Format dates as "mm/dd/yyyy"
        existing_date_str = existing_date.strftime('%m/%d/%Y')
        new_date_str = new_date.strftime('%m/%d/%Y')

        # Create PDF document
        current_date_str = datetime.now().strftime("%m%d%Y")

        pdf_filename = f'F:/Data Base/renew Box/{box_number}_{current_date_str}.pdf'

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Define styles
        styles = getSampleStyleSheet()
        current_date_str = datetime.now().strftime("%m/%d/%Y")

        # Create a title paragraph
        title = Paragraph(f'<u>Renewal Receipt for Box {box_number} - {current_date_str}</u>', styles['Title'])

        # Create a table object and style for the first table
        table_data = [
            ['Parameter', 'Value'],
            ['Box Number', box_number],
            ['Size', size_display],  # Displayed value based on conditions
            ['Current Due Date', existing_date_str],
            ['Months to Add', str(months_to_add)],
        ]

        # Only include the row for free months if the user selected 'Y'
        if add_free_months == 'Y':
            table_data.append(['Free Months adding as discount', str(free_months)])

        # Continue with the rest of the table_data
        table_data += [
            ['New Due Date', new_date_str],
            ['Calculated Price', f"${price}"],
            ['Payment Method', payment_method]
        ]

        table = Table(table_data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),  # Exclude the line between the first and second row
            ('GRID', (0, -1), (-1, -1), 1, colors.black)  # Include the line at the bottom
        ]))

        # Create a table object for the second table (Name)
        name_table_data = [
            ['Names Under this BOX number'],
            *[[name] for name in result['Name'].tolist()]
        ]

        name_table = Table(name_table_data, colWidths=[400])
        name_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Create a table object for the third table (Signatures)
        bottom_table_data = [
            ['Mailzib Rep:', representative_name, 'Client Name:', ''],
            ['Signature:', '', 'Signature:', ''],
            ['Date:', '', 'Date:', '']
        ]

        # Increase the height of the second row (index 1) for the Signature
        row_heights = [30,  # Height for the first row
                       70,  # Increased height for the second row
                       30]  # Height for the third row

        bottom_table = Table(bottom_table_data, colWidths=[100, 150, 100, 150], rowHeights=row_heights)
        bottom_table.setStyle(TableStyle([
            ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),  # Set vertical alignment to MIDDLE for the second row
            ('VALIGN', (0, 2), (-1, 2), 'MIDDLE'),  # Set vertical alignment to MIDDLE for the Date row
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 1), (-1, -1), 1, colors.black),  # Include a line above the second row
            ('GRID', (0, 2), (-1, -1), 1, colors.black)  # Include a line above the third row
        ]))

        # Build the PDF
        elements = [title, Spacer(1, 0.25 * 72), table, Spacer(1, 0.25 * 72), name_table, Spacer(1, 0.25 * 72),
                    bottom_table]

        # Add text for the address under the last table
        # Add text for the address under the last table
        address_text = (
            "23016 Lake Forest Dr,<br/>"
            "Laguna Hills, CA, 92653.<br/>"
            "Tel: (949) 246-6438<br/>"
            "Email: Mailzibstore@gmail.com"
        )

        address_paragraph = Paragraph(address_text, styles['Normal'])
        elements.append(Spacer(1, 0.25 * 72))
        elements.append(address_paragraph)

        doc.build(elements)

        # Extract 'Name' from the result DataFrame
        name_value = result.loc[result.index[0], 'Name']

        current_date_str_formatted = datetime.now().strftime("%m/%d/%Y")

        # Add information to the accounting.csv file
        accounting_data = pd.DataFrame({
            'Row': [0],  # Placeholder for now
            'Box number': [box_number],
            'Name': [name_value],
            'Date': [current_date_str],
            'Reason': ['Renewal'],
            'Pay method': [payment_method],
            'Income': [price],
            'Expense': [0]  # You can adjust this value as needed
        })

        existing_data = pd.read_csv(ACCOUNTING_FILE_PATH)

        # If the DataFrame is empty, set the "Row" value to 1
        if existing_data.empty:
            accounting_data['Row'] = 1
        else:
            # Find the maximum value in the "Row" column
            max_row_value = existing_data['Row'].max()

            # Increment the "Row" value for the new row
            new_row_value = max_row_value + 1
            accounting_data['Row'] = new_row_value

        # Append the new data to the DataFrame
        combined_data = pd.concat([existing_data, accounting_data], ignore_index=True)

        # Write the combined DataFrame back to the CSV file
        combined_data.to_csv(ACCOUNTING_FILE_PATH, index=False)

        return f"Renewal report generated: {pdf_filename}"

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
        result = data[result_mask].copy()  # Make a copy to avoid the SettingWithCopyWarning

        if result.empty:
            return f"No data found within the specified date range with 'Got New Key' set to 'ok."

        current_datetime = datetime.now()

        # Format the current date and time to include it in the filename
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        # Create a PDF file on your desktop with the generated filename
        pdf_filename = f"F:/Data Base/renew/Renewing_table_{formatted_datetime}.pdf"

        # Define a custom page size to reduce the top margin
        custom_page_size = landscape(letter)

        # Adjust the top margin as needed (0.5 inch in this case)
        top_margin = 0.25 * 72  # 0.5 inch = 36 points
        doc = SimpleDocTemplate(pdf_filename, pagesize=custom_page_size, topMargin=top_margin)

        # Format the 'Date' column to "mm/dd/yyyy" format using .loc
        result['Date'] = result['Date'].dt.strftime('%m/%d/%Y')

        # Calculate the count of unique "box number"
        unique_box_count = result['Box number'].nunique()

        # Define the table data
        table_data = [result.columns] + result.values.tolist()

        # Create a table object and style
        table = Table(table_data, colWidths=[100] * len(result.columns))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Build the PDF
        elements = [
            Paragraph(
                f"Renew list between {start_date.strftime('%m/%d/%Y')} and {end_date.strftime('%m/%d/%Y')}, we have {unique_box_count} unique Box_number."),
            Spacer(1, 0.25 * 72),  # Add 0.5-inch space before the table
            table
        ]
        doc.build(elements)

        return f"Search result saved as PDF: {pdf_filename}"

    except Exception as e:
        return str(e)


def add_new_box(new_box_data):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the "Box number" and convert it to an integer
        new_box_number = int(new_box_data["Box number"])

        # Check if "Box number" already exists
        if new_box_number in data["Box number"].values:
            # Box number already exists, return an error message
            return f"Error: Box number {new_box_number} already exists and cannot open a new box for this number."

        # Define the "Type" based on the "Box number" ranges
        box_number_ranges = [
            (101, 280, "S"),
            (281, 344, "M"),
            (345, 364, "B"),
            (365, 396, "M"),
            (397, 420, "B"),
            (421, 508, "M"),
            (509, 563, "S")
        ]

        # Find the appropriate "Type" based on the "Box number"
        box_type = next((box_type for start, end, box_type in box_number_ranges if start <= new_box_number <= end),
                        None)

        if box_type is None:
            return "Error: Box number does not fall within any specified range."

        # Find the position to insert the new box number
        existing_box_numbers = data["Box number"].unique()
        existing_box_numbers = [int(box_num) for box_num in existing_box_numbers]
        positions = [i for i, num in enumerate(existing_box_numbers) if num < new_box_number]
        if positions:
            insert_position = max(positions) + 1
        else:
            insert_position = 0

        # Create a new DataFrame for the box
        got_new_key_input = new_box_data["Did get new key?"].strip().lower()
        got_new_key = "Ok" if got_new_key_input == "y" else ""

        new_row = pd.DataFrame({
            "Box number": [new_box_number],
            "Type": [box_type],  # Assign the determined "Type"
            "Name": [new_box_data["Name"]],
            "Date": [pd.to_datetime(new_box_data["Date"], format='%m/%d/%Y', errors='coerce').strftime('%m/%d/%Y')],
            "Phone": [new_box_data["Phone"]],
            "Got New Key": [got_new_key],
            "Information": [new_box_data["Information"]]
        })

        # Check if "Got New Key" is either "ok" (case-insensitive) or empty
        if got_new_key_input == "y" or got_new_key_input == "n" or got_new_key_input == "":
            # Concatenate the new DataFrame with the existing data
            data = pd.concat([data.iloc[:insert_position], new_row, data.iloc[insert_position:]], ignore_index=True)

            # Sort the DataFrame by "Box number"
            data = data.sort_values(by="Box number").reset_index(drop=True)

            # Save the updated DataFrame to the CSV file
            data.to_csv(CSV_FILE_PATH, index=False, date_format='%m/%d/%Y')

            return f"New box with Box number {new_box_number} and Type {box_type} has been added."
        else:
            return "Error: 'Did get new key?' can only be 'Y' (case-insensitive), 'N', or left empty."

    except Exception as e:
        return str(e)


def add_name_to_box(box_number, name, phone=None):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Clean the "Box number" and convert it to an integer
        box_number = int(box_number)

        if box_number not in data["Box number"].values:
            return f"Box number {box_number} does not exist. Please use the 'add_new_box' method to add a new box."

        # Find the position to insert the new box with the given "Box number"
        insert_position = data[data["Box number"] == box_number].index[0] + 1

        # Create a new row with "Box number," "Name," and optionally "Phone," leaving other columns empty
        new_row_data = {
            "Box number": [box_number],
            "Type": [""],
            "Name": [name],
            "Date": [""],
            "Got New Key": [""],
            "Information": [""]
        }

        if phone is not None:
            new_row_data["Phone"] = [phone]

        new_row = pd.DataFrame(new_row_data)

        # Concatenate the new row with the existing data at the specified position
        data = pd.concat([data.iloc[:insert_position], new_row, data.iloc[insert_position:]], ignore_index=True)

        # Save the updated DataFrame to the CSV file
        data.to_csv(CSV_FILE_PATH, index=False)

        return f"New row with Box number {box_number}, Name '{name}', and Phone '{phone}' has been added."

    except Exception as e:
        return str(e)


def delete_box_by_number(box_number):
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Check if the given box number exists in the DataFrame
        if box_number not in data["Box number"].values:
            return f"No boxes with Box number {box_number} found."

        # Prompt the user for confirmation
        confirmation = input(f"Are you sure you want to delete box number {box_number}? (Y/N): ").upper()

        if confirmation == "Y":
            # Delete all rows with the given box number
            data = data[data["Box number"] != box_number]

            # Save the updated DataFrame to the CSV file
            data.to_csv(CSV_FILE_PATH, index=False)

            return f"All boxes with Box number {box_number} have been deleted."
        elif confirmation == "N":
            return "Deletion canceled. No boxes have been deleted."
        else:
            return "Invalid input. Please enter 'Y' for Yes or 'N' for No."

    except Exception as e:
        return str(e)


def delete_row_by_name():
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Ask for the box number to delete
        box_number = input("Enter the box number for which you want to delete a name: ")
        try:
            box_number = int(box_number)
        except ValueError:
            return "Invalid input. Please enter a valid box number."

        # Filter data for the given box number
        box_data = data[data["Box number"] == box_number]

        if box_data.empty:
            return f"No data found for Box number {box_number}."

        # Display the names with numbers
        names_with_numbers = {i + 1: name for i, name in enumerate(box_data["Name"].tolist())}
        for num, name in names_with_numbers.items():
            print(f"{num}. {name}")

        # Ask the user which name to delete
        selected_number = input("Enter the number corresponding to the name you want to delete: ")
        try:
            selected_number = int(selected_number)
            if 1 <= selected_number <= len(names_with_numbers):
                selected_name = names_with_numbers[selected_number]
            else:
                return "Invalid number selected. Please enter a valid number."
        except ValueError:
            return "Invalid input. Please enter a valid number."

        # Ask for confirmation
        confirmation = input(
            f"Are you sure you want to delete the row with Box number {box_number} and Name {selected_name}? (Y/N): ").strip().lower()
        if confirmation == 'y':
            # Delete rows with the selected box number and name
            data = data[(data["Box number"] != box_number) | (data["Name"] != selected_name)]

            # Convert all columns to strings
            data = data.astype(str)

            # Save the updated DataFrame to the CSV file with date format
            data.to_csv(CSV_FILE_PATH, index=False, date_format='%m/%d/%Y')

            return f"Row with Box number {box_number} and Name {selected_name} has been deleted."
        else:
            return "Deletion canceled."

    except Exception as e:
        return str(e)


def display_info_by_status_as_pdf():
    try:
        # Load the CSV file into a DataFrame using a comma (,) as the delimiter
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Filter rows where 'Got New Key' is 'ok'
        ok_mask = data['Got New Key'].str.strip().str.lower() == 'ok'

        # Get the unique 'Box numbers' with 'Got New Key' as 'ok'
        ok_box_numbers = data.loc[ok_mask, 'Box number'].unique()

        # Filter the data to include all rows with 'Box number' in the above list
        filtered_data = data[data['Box number'].isin(ok_box_numbers)]

        # Further filter data to only include rows with 'Got New Key' as 'ok'
        key_ok_data = data[ok_mask]

        if filtered_data.empty:
            return "No data found with 'Got New Key' set to 'ok.'"

        # Count unique 'Box numbers' in the filtered data
        unique_box_numbers = len(key_ok_data['Box number'].unique())

        # Count the number of rows for each type (s, m, b) ignoring case
        s_count = key_ok_data[key_ok_data['Type'].str.lower() == 's'].shape[0]
        m_count = key_ok_data[key_ok_data['Type'].str.lower() == 'm'].shape[0]
        b_count = key_ok_data[key_ok_data['Type'].str.lower() == 'b'].shape[0]

        # Define a custom page size
        custom_page_size = landscape(letter)

        # Adjust the top margin as needed (0.5 inch in this case)
        top_margin = 0.25 * 72  # 0.5 inch = 36 points

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the current date and time to include it in the filename
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        # Define the output PDF filename with the specified path and current date
        pdf_filename = f"F:/Data Base/active/active_box_table_{formatted_datetime}.pdf"

        # Create the PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=custom_page_size, topMargin=top_margin)

        # Create a list of elements to build the PDF
        elements = []

        # Add text information at the top
        info_text = f"List of Active BOX\n"
        info_text += f"Total Box numbers that Got New Keys: {unique_box_numbers}\n"
        info_text += f"Total Small Boxes: {s_count}\n"
        info_text += f"Total Medium Boxes: {m_count}\n"
        info_text += f"Total Big Boxes: {b_count}\n\n"
        elements.append(Paragraph(info_text, getSampleStyleSheet()['Normal']))

        # Create a table from filtered_data with grid lines
        table_data = [filtered_data.columns.tolist()] + filtered_data.values.tolist()

        # Define new column widths
        col_widths = [
            60 if col in ['Box number', 'Got New Key', 'Type', 'Date', 'phone'] else
            200 if col in ['Name', 'Information'] else
            100 for col in filtered_data.columns
        ]
        table = Table(table_data, colWidths=col_widths)

        # Define the table style with grid lines
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Add the table to the elements
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        return f"Search result saved as PDF: {pdf_filename}"

    except Exception as e:
        return str(e)


def back_up():
    try:
        # Load the CSV file into a DataFrame using the same CSV file path
        data = pd.read_csv(CSV_FILE_PATH, delimiter=',')

        # Define a custom page size with landscape orientation
        custom_page_size = landscape(letter)

        # Adjust the left margin as needed (0.25 inch in this case)
        left_margin = 0.25 * 72  # 0.25 inch = 18 points

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the current date and time to include it in the filename
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        # Define the output PDF filename with the specified path and current date
        pdf_filename = f"F:/Data Base/backup/Back up-{formatted_datetime}.pdf"

        # Create a list to store table data
        table_data = [data.columns.tolist()]  # First row with column names
        table_data.extend(data.values.tolist())  # Data rows

        # Specify the column widths (in points) to fit within the page
        col_widths = [100] * len(data.columns)

        # Create a table object with specified column widths
        table = Table(table_data, colWidths=col_widths)

        # Set table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Create a PDF document with left and right margins and adjusted left margin
        doc = SimpleDocTemplate(pdf_filename, pagesize=custom_page_size,
                                leftMargin=left_margin, rightMargin=20, topMargin=20, bottomMargin=20)

        # Build the PDF
        elements = [table]
        doc.build(elements)

        return f"CSV file converted to PDF: {pdf_filename}"

    except Exception as e:
        return str(e)


def update_box_by_number(box_number):
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

        # Display existing values
        existing_values = data.loc[result.index[0]].to_dict()
        print("Existing values:")
        for key, value in existing_values.items():
            if key != "Box number" and key != "Due date":
                print(f"{key}: {value}")

        updated_box_data = {}
        for key in existing_values.keys():
            if key != "Box number" and key != "Due date" and key != "Type":  # Exclude "Type"
                if key == "Got New Key":
                    update_field = input(f"Do you want to update {key}? (Y/N): ").strip().lower()
                    if update_field == 'y':
                        got_new_key = input("Did get a new key? (Y/N): ").strip().lower()
                        if got_new_key == 'y':
                            updated_box_data[key] = "Ok"
                        elif got_new_key == 'n':
                            updated_box_data[key] = ""
                        else:
                            return "Error: Invalid input. Please enter 'Y' or 'N'."
                    else:
                        updated_box_data[key] = existing_values[key]
                else:
                    update_field = input(f"Do you want to update {key}? (Y/N): ").strip().lower()
                    if update_field == 'y':
                        new_value = input(f"Enter the new value for {key}: ")
                        updated_box_data[key] = new_value
                    else:
                        updated_box_data[key] = existing_values[key]

        # Update all column values for the first matching row
        for key, value in updated_box_data.items():
            data.at[result.index[0], key] = value

        # Save the updated DataFrame to the CSV file with date format
        data.to_csv(CSV_FILE_PATH, index=False, date_format='%m/%d/%Y')

        return f"Box number {box_number} has been updated with new values."

    except Exception as e:
        return str(e)


def move_rows():
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(CSV_FILE_PATH)

        # Convert the 'Date' column to datetime format for easier comparison
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Convert the 'Got New Key' column to lowercase for case-insensitive comparison
        df['Got New Key'] = df['Got New Key'].str.lower()

        # Sort the DataFrame based on 'Box number' and 'Date'
        df.sort_values(['Box number', 'Date'], ascending=[True, False], inplace=True)

        # Group by 'Box number' and move the row with 'Got New Key' equal to 'ok' to the top
        df = df.groupby('Box number').apply(
            lambda x: x.sort_values('Date', ascending=False) if any(x['Got New Key'] == 'ok') else x)

        # Reset the index of the DataFrame
        df.reset_index(drop=True, inplace=True)

        # Format the 'Date' column to 'mm/dd/yyyy'
        df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

        # Save the modified DataFrame to the same CSV file
        df.to_csv(CSV_FILE_PATH, index=False)

        return "Rows moved successfully."
    except Exception as e:
        return f"Error moving rows: {str(e)}"


def add_entry_to_accounting():
    try:
        # Get user input for each field
        name = input("Enter Name: ")
        date_str = input("Enter Date (MM/DD/YYYY): ")
        reason = input("Enter Reason: ")
        pay_method = input("Enter Pay Method: ")

        # Get user input for Income and set to 0 if not provided
        income_input = input("Enter Income (leave blank for 0): ")
        income = float(income_input) if income_input else 0

        # Get user input for Expense and set to 0 if not provided
        expense_input = input("Enter Expense (leave blank for 0): ")
        expense = float(expense_input) if expense_input else 0

        # Get user input for Deposit and set to 0 if not provided
        deposit_input = input("Enter Deposit (leave blank for 0): ")
        deposit = float(deposit_input) if deposit_input else 0

        # Get user input for Withdrawal and set to 0 if not provided
        withdrawal_input = input("Enter Withdrawal (leave blank for 0): ")
        withdrawal = float(withdrawal_input) if withdrawal_input else 0

        # Parse the date string to a datetime object
        try:
            date = datetime.strptime(date_str, "%m/%d/%Y").strftime("%m/%d/%Y")
            print("Parsed date:", date)
        except ValueError as ve:
            return f"Error parsing date: {ve}"

        # If the accounting CSV file exists, read it; otherwise, create a new DataFrame
        if os.path.exists(ACCOUNTING_FILE_PATH):
            existing_data = pd.read_csv(ACCOUNTING_FILE_PATH, delimiter=',')
        else:
            existing_data = pd.DataFrame(
                columns=['Row', 'Box number', 'Name', 'Date', 'Reason', 'Pay method', 'Income', 'Expense'])

        # If there are no existing rows, set the new "Row" value to 1
        if existing_data.empty:
            new_row_value = 1
        else:
            # Generate the "Row" column by incrementing the maximum value by 1
            max_row_number = existing_data['Row'].max()
            new_row_value = max_row_number + 1

        # Add the new entry with the calculated "Row" value
        new_entry = pd.DataFrame({
            'Row': [new_row_value],
            'Box number': [""],  # Leave it empty or provide a default value
            'Name': [name],
            'Date': [date],
            'Reason': [reason],
            'Pay method': [pay_method],
            'Income': [income],
            'Expense': [expense],
            'Deposit': [deposit],
            'Withdrawal': [withdrawal]
        })

        # Concatenate the DataFrames with the new row at the bottom
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True, sort=False)

        print("Last added row:\n", updated_data.iloc[-1])  # Print only the last row

        # Write the updated data to the accounting CSV file
        updated_data.to_csv(ACCOUNTING_FILE_PATH, index=False)

        return "Entry added successfully."

    except KeyboardInterrupt:
        # Handle the KeyboardInterrupt (Ctrl+C) gracefully
        return "Operation canceled by the user."

    except Exception as e:
        return str(e)


def back_up_accounting(column_widths=None) -> str:
    try:
        # Load the CSV file into a DataFrame using the same CSV file path
        data = pd.read_csv(ACCOUNTING_FILE_PATH, delimiter=',')

        # Convert the "Box number" column to numeric, handling non-finite values
        data['Box number'] = pd.to_numeric(data['Box number'], errors='coerce').fillna(0).astype(int)

        # Convert 'Deposit' and 'Withdrawal' columns to numeric, handling ',' as thousand separator
        data['Deposit'] = pd.to_numeric(data['Deposit'].replace({',': ''}, regex=True), errors='coerce').fillna(0)
        data['Withdrawal'] = pd.to_numeric(data['Withdrawal'].replace({',': ''}, regex=True), errors='coerce').fillna(0)

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the current date and time to include it in the filename
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        # Define the output PDF filename with the specified path and current date
        pdf_filename = f"F:/Data Base/accounting/Accounting-{formatted_datetime}.pdf"

        # Create a list to store table data
        table_data = [data.columns.tolist()]  # First row with column names
        # Split column names with two words into two lines
        for col_index, col_name in enumerate(data.columns):
            if ' ' in col_name:
                # If the column name contains a space, split it into two lines
                col_name_parts = col_name.split(' ')
                table_data[0][col_index] = col_name_parts[0] + '\n' + col_name_parts[1]

        table_data.extend(data.values.tolist())  # Data rows

        # Add a summary row
        income_sum = round(data['Income'].sum(), 2)
        expense_sum = round(data['Expense'].sum(), 2)
        balance = round(income_sum - expense_sum, 2)

        # Check if 'Deposit' and 'Withdraw' columns exist in the DataFrame
        if 'Deposit' in data.columns and 'Withdrawal' in data.columns:
            deposit_sum = round(data['Deposit'].sum(), 2)
            withdraw_sum = round(data['Withdrawal'].sum(), 2)
            total_summary_row = round((income_sum + deposit_sum) - (withdraw_sum + expense_sum))
        else:
            # Handle the case where 'Deposit' or 'Withdrawal' columns are missing
            deposit_sum = 0
            withdraw_sum = 0
            total_summary_row = 0

        summary_row = [
            'Total',
            f"Income: {income_sum:.2f}",
            f"Expense: {expense_sum:.2f}",
            f"Balance: {balance:.2f}",
            f"Summary of Deposit: {deposit_sum:.2f}",
            f"Summary of Withdraw: {withdraw_sum:.2f}",
            f"Total Summary Row: {total_summary_row:.2f}"
        ]
        table_data.append(summary_row)

        # Remove the last row (summary row)
        table_data.pop()

        # Specify the column widths (in points) to fit within the page
        if column_widths is None:
            # Default column widths if not provided
            column_widths = [25, 40, 110, 60, 180, 50, 60, 60, 60, 60]  # Adjust the widths as needed

        # Create a table object with specified column widths
        table = Table(table_data, colWidths=column_widths)

        # Set table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Create a PDF document with left and right margins
        doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter),
                                leftMargin=72, rightMargin=72, topMargin=20, bottomMargin=20)

        # Build the PDF
        elements = [table]

        # Add a bit of space between the table and the following elements
        elements.append(Spacer(1, 20))  # Adjust the height of the space as needed

        # Add Summary of Income, Expense, and Balance
        style = getSampleStyleSheet()['Normal']
        elements.append(Paragraph(f"Summary of Income: {income_sum:.2f}", style))
        elements.append(Paragraph(f"Summary of Expense: {expense_sum:.2f}", style))
        elements.append(Paragraph(f"Summary of Balance: {balance:.2f}", style))
        elements.append(Paragraph(f"Summary of Deposit: {deposit_sum:.2f}", style))
        elements.append(Paragraph(f"Summary of Withdraw: {withdraw_sum:.2f}", style))
        elements.append(Paragraph(f"Total Summary Row: {total_summary_row:.2f}", style))

        doc.build(elements)

        return f"CSV file converted to PDF: {pdf_filename}"

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"












