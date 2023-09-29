import os
import sys
import time
import requests
import argparse

def main():
    def upload_csv(base_url, object_type, object_id, filename, token, overwrite_values):
        file_path = os.path.join("csv_upload_files", filename)  # Construct file path from filename
        url = f"https://{base_url}/integration/v1/data_dictionary/{object_type}/{object_id}/upload/"
        headers = {"TOKEN": token}

        try:
            with open(file_path, "rb") as file:
                print(f"Uploading file: {file_path}")  # Printing the file path being used
                print(f"File type: {'text/csv'}")  # Printing the file type
                
                files = {"file": (filename, file, 'text/csv')}  # Explicitly setting the content type to text/csv
                params = {"overwrite_values": overwrite_values}
                response = requests.put(url, headers=headers, files=files, params=params)

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
                    time.sleep(5)
        except requests.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
            sys.exit(1)

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

    # Validate the file existence
    if not os.path.exists(os.path.join("csv_upload_files", args.filename)):
        print(f"The file '{args.filename}' does not exist in the 'csv_upload_files' directory.")
        sys.exit(1)

    task_id = upload_csv(args.base_url, args.object_type, args.object_id, args.filename, args.token, args.overwrite_values)
    if task_id:
        check_job_status(args.base_url, task_id, args.token)

if __name__ == "__main__":
    main()
