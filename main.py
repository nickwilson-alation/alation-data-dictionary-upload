import os
import sys
import time
import requests
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from html import escape

CSV_UPLOAD_FILES_PATH = "csv_upload_files"
SANITIZED_FILE_PREFIX = "sanitized_"
POLL_INTERVAL_IN_SECONDS = 2

# Sanitizes HTML to work around a python-magic library issue on the backend
def sanitize_html(text):
    if pd.isna(text):
        return text
    soup = BeautifulSoup(text, "html.parser")
    return escape(soup.get_text()) if soup.find() else text

# Lowercases all the headers in the DataFrame to work around mixed-case-sensitive backend
def lowercase_headers(df):
    df.columns = [col.lower() for col in df.columns]
    return df

def upload_csv(base_url, object_type, object_id, filename, token, overwrite_values):
    file_path = os.path.join(CSV_UPLOAD_FILES_PATH, SANITIZED_FILE_PREFIX + filename)  # Construct file path from filename
    url = f"https://{base_url}/integration/v1/data_dictionary/{object_type}/{object_id}/upload/"
    headers = {"TOKEN": token}

    try:
        with open(file_path, "rb") as file:
            files = {"file": (filename, file)}
            data = {"overwrite_values": overwrite_values}
            response = requests.put(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        job = response.json()
        print("Upload job created:", job)
        return job['task']['id']
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response text: {err.response.text}")  # This will provide more detail on the error
    except Exception as err:
        print(f"An error occurred: {err}")
        sys.exit(1)

def check_job_status(base_url, task_id, token):
    url = f"https://{base_url}/integration/v1/data_dictionary/tasks/{task_id}"
    headers = {"TOKEN": token}

    try:
        while True:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            job_status = response.json()
            print("Job Status:", job_status['state'], "-", job_status['status'] if 'status' in job_status else "")

            if job_status['state'] == "COMPLETED":
                print("Job completed.")
                return job_status
            elif job_status['state'] == "PROCESSING":
                print("Progress:", job_status['progress']['number_of_batches_completed'], "/", job_status['progress']['total_number_of_batches'])
                time.sleep(POLL_INTERVAL_IN_SECONDS)
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Upload CSV to Alation Data Dictionary")
    parser.add_argument("--filename", required=True, help="Filename of the CSV")
    parser.add_argument("--base-url", required=True, help="Alation base URL")
    parser.add_argument("--object-type", required=True, choices=["data", "schema", "table"], help="Object type")
    parser.add_argument("--object-id", required=True, type=int, help="Object ID")
    parser.add_argument("--token", default=os.environ.get("ALATION_TOKEN", None), help="Alation API token")
    parser.add_argument("--overwrite-values", type=bool, default=False, help="Overwrite values")

    args = parser.parse_args()

    # Validate the token
    if not args.token:
        print("Please provide Alation API token either through --token option or ALATION_TOKEN environment variable.")
        sys.exit(1)

    # Validate the file existence and sanitize HTML before uploading
    file_path = os.path.join(CSV_UPLOAD_FILES_PATH, args.filename)
    if os.path.exists(file_path):
        # Sanitize the CSV and create a new sanitized file for uploading 
        original_file_path = os.path.join(CSV_UPLOAD_FILES_PATH, args.filename) 
        sanitized_file_path = os.path.join(CSV_UPLOAD_FILES_PATH, SANITIZED_FILE_PREFIX + args.filename) 
        df = pd.read_csv(original_file_path, dtype=str)
        df = lowercase_headers(df)
        df = df.applymap(lambda x: sanitize_html(x) if isinstance(x, str) else x) 
        df.to_csv(sanitized_file_path, index=False, quoting=3)  # Quoting=3 ensures all field values are surrounded by quotes
    else:
        print(f"The file '{args.filename}' does not exist in the '{CSV_UPLOAD_FILES_PATH}' directory.")
        sys.exit(1)

    task_id = upload_csv(args.base_url, args.object_type, args.object_id, args.filename, args.token, args.overwrite_values)
    if task_id:
        check_job_status(args.base_url, task_id, args.token)

if __name__ == "__main__":
    main()
