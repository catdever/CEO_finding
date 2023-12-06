from openai import OpenAI
import csv
import pandas as pd
import os

# Set your OpenAI API key
client = OpenAI(
    # os.environ.get("OPENAI_API_KEY") # You can set in .env file
    api_key="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" # Change to Your Key
)

def get_manager_name(company_name):
    # Use the OpenAI API to generate a manager's name based on the company name
    prompt = f'''I only want to know the full name of the CEO of the company below without any explanation.
        The company's name is {company_name}.
        Do not add any other words, give me only the full name of the company's CEO without any explanation. 
        Don't add any explanation, only tell me full name or none if you don't know.'''
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}]
    )

    manager_name = response['choices'][0]['text'].strip() # there will be some errors
    # manager_name = response.choices[0].message.content.strip() # if above row doesn't work, try this
    # manager_name = response.choices[0].text.strip() # if above row doesn't work, try this
    return manager_name

def process_csv_file(input_file):
    # Read the CSV file using the csv module
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Get the fieldnames from the header
        fieldnames = reader.fieldnames

        # Create a new field for the manager names
        fieldnames.append('Manager_Name')

        # Create a list to store rows
        rows = []

        # Iterate through each row and get the manager's name using OpenAI API
        for row in reader:
            print(row)
            company_name = row.get('CAUSE_NAME')  # You can change the letter 'A' if you want
            print(company_name)
            manager_name = get_manager_name(company_name)
            
            # Add the B to the row
            row['Manager_Name'] = manager_name

            # Append the updated row to the list
            rows.append(row)

    # Write the updated rows back to the CSV file
    with open(input_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        # Write the updated rows
        writer.writerows(rows)

if __name__ == "__main__":
    # Get the input CSV file dynamically (change the filename as needed)
    input_csv_file = input("Enter the path to the input CSV file: ")

    # Process the CSV file and store manager names, overwriting the input file
    process_csv_file(input_csv_file)

    print("Processing complete. Manager names added to the CSV file.")