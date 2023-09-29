# Alation Data Dictionary Upload Script

This Python script allows users to easily upload CSV files to Alation's Data Dictionary via API.

## Requirements

- Python
- `requests` library (Install with `pip install requests`)

## Usage

1. Place your CSV files in the `csv_upload_files/` directory.
2. Run the script with the necessary arguments.

### Arguments

- `filename`: The name of the CSV file (located in `csv_upload_files/`)
- `base_url`: Your Alation base URL
- `object_type`: Object type - choose from "data", "schema", or "table"
- `object_id`: Object ID (integer)
- `--token`: (Optional) Alation API token. Can also be set as an environment variable `ALATION_TOKEN`
- `--overwrite_values`: (Optional) Boolean to overwrite values, defaults to False

### Sample Command with Placeholders

Use the following format to run the script, replacing the placeholders with your actual values.

`python {{script_name}} {{filename}} {{base_url}} {{object_type}} {{object_id}} --token {{your_token}} --overwrite_values {{True_or_False}}`

### Example Command with Bogus Values

Here’s an example command with made-up values to illustrate how to replace the placeholders.

`python upload_to_alation.py myfile.csv alation.example.com data 123 --token abc123def456ghi789 --overwrite_values True`

## Additional Information

This script simplifies the process of uploading CSV files to the Alation Data Dictionary. Make sure to follow the argument guidelines and replace the placeholders with your specific information. Always ensure the CSV files are placed in the `csv_upload_files/` directory, which is ignored by Git for user privacy and security.

For any further queries or issues, please refer to the official Alation API documentation or contact support.
