import pandas as pd

# Replace 'input_excel_file.xlsx' with your Excel file path
excel_file = '/Users/myouse652/Desktop/Main.xlsx'

# Replace 'output_csv_file.csv' with the desired CSV file path and name
csv_file = '/Users/myouse652/Desktop/Main1.csv'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file)

# Save the DataFrame to a CSV file
df.to_csv(csv_file, index=False)

