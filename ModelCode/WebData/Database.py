import csv

# Initialize an empty dictionary to store data
area_data = []

# Read data from the CSV file
with open('Data/HTML data/area data.csv', 'r') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)

    # Skip the header row

    for row in csvreader:
        # Extract data from the row

        area_name = row[0]
        image = row[1]
        avg_sell_price = row[2]
        house_price = row[3]
        avg_rent_price = row[4]

        if row[0] != 'Area Name':
            area_data.append(row)


