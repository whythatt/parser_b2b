import csv
import json

# Load JSON data from the file
with open("company_numbers.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open("company_numbers.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(["company_name", "company_number"])

    # Iterate through each city in the JSON data
    for city, companies in data.items():
        for company in companies:
            # Write each company's name and number to the CSV
            writer.writerow([company["company_name"], company["company_number"]])
