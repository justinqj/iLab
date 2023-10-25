import json

# List of years
years = range(2019, 2024)

all_data = []

# Loop through each year and read the corresponding file
for year in years:
    file_name = f"raw_output_{year}.json"
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_data.extend(data)

# Write the combined data to the output file
output_file = "raw_output.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f"Combined all files into {output_file}")
