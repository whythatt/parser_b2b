import csv
import json

# Load JSON data from the file
<<<<<<< HEAD
with open("company_numbers_тверь.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open("company_numbers_тверь.csv", "w", newline="", encoding="utf-8") as csv_file:
=======
with open("company_numbers_спб.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open("company_numbers_спб.csv", "w", newline="", encoding="utf-8") as csv_file:
>>>>>>> b061450 (test)
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(["company_name", "company_number", "category", "website"])

    # Iterate through each city in the JSON data
    for city, companies in data.items():
        for company in companies:
            # Write each company's name and number to the CSV
            writer.writerow(
                [
                    company["company_name"],
                    company["company_number"],
                    company["category"],
                    company["website"],
                    city,
                ],
            )
