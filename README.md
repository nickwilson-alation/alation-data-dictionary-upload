# NOTE - This repo is no longer maintained as of January 2024.

This repo was created as a workaround for a bug, but is no longer relevant as the bug has been resolved in the latest versions of Alation. This script is untested against newer versions of Alation.

# Alation Data Dictionary Upload Script

This Python script allows users to easily upload CSV files to Alation's Data Dictionary via API.

## Requirements

- Python
- `requests` library (Install with `pip install -r requirements.txt`)

## Usage

1. Place your CSV files in the `csv_upload_files/` directory.
2. Run the script with the necessary arguments.

### Arguments

- `--filename`: The name of the CSV file (located in `csv_upload_files/`)
- `--base_url`: Your Alation base URL
- `--object_type`: Object type - choose from "data", "schema", or "table"
- `--object_id`: Object ID (integer)
- `--token`: (Optional) Alation API token. Can also be set as an environment variable `ALATION_TOKEN`
- `--overwrite_values`: (Optional) Boolean to overwrite values, defaults to False

### Sample Command with Placeholders

Use the following format to run the script, replacing the placeholders with your actual values.

`python main.py --filename {{filename}} --base-url {{base_url}} --object-type {{object_type}} --object-id {{object_id}} --token {{your_token}} --overwrite-values {{True_or_False}}`

### Example Command with Bogus Values

Here’s an example command with made-up values to illustrate how to replace the placeholders.

`python main.py --filename myfile.csv --base-url alation.example.com --object-type data --object-id 123 --token abc123def456ghi789 --overwrite-values True`


## Additional Information

This script simplifies the process of uploading CSV files to the Alation Data Dictionary. Make sure to follow the argument guidelines and replace the placeholders with your specific information. Always ensure the CSV files are placed in the `csv_upload_files/` directory, which is ignored by Git for user privacy and security.

For any further queries or issues, please refer to the official Alation API documentation or contact support.

## Disclaimer

This project and all the code contained within this repository is provided "as is" without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the project is with you.

The author, including Alation, shall not be responsible for any damages whatsoever, including direct, indirect, special, incidental, or consequential damages, arising out of or in connection with the use or performance of this project, even if advised of the possibility of such damages.

Please understand that this project is provided for educational and informational purposes only. Always ensure proper testing, validation and backup before implementing any code or program in a production environment.

By using this project, you accept full responsibility for any and all risks associated with its usage.
