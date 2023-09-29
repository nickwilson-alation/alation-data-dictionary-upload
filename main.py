import os
import sys
import time
import requests
import argparse

def main():
    def upload_csv(alation_domain, object_type, object_id, file_path, token, overwrite_values):
        url = f"https://{alation_domain}/integration/v1/data_dictionary/{object_type}/{object_id}/upload/"
        headers = {"Authorization": f"Token {token}"}

        try:
            with open(file_path, "rb") as file:
                files = {"file": (os.path.basename(file_path), file)}
                params = {"overwrite_values": overwrite_values}
                response = requests.put(url, headers=headers, files=files, params=params)

            response.raise_for_status()  # Raise an exception for HTTP errors

            job = response.json()
            print("Upload job created:", job)
            return job['id']
        except requests.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
            sys.exit(1)

    # Function to check the status of the upload job
    def check_job_status(alation_domain, task_id, token):
        url = f"https://{alation_domain}/integration/v1/data_dictionary/tasks/{task_id}/"
        headers = {"Authorization": f"Token {token}"}
        
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

    # Command-line arguments setup
    parser = argparse.ArgumentParser(description="Upload CSV to Alation Data Dictionary")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("alation_domain", help="Alation domain")
    parser.add_argument("object_type", choices=["data", "schema", "table"], help="Object type")
    parser.add_argument("object_id", type=int, help="Object ID")
    parser.add_argument("--token", default=os.environ.get("ALATION_TOKEN", None), help="Alation API token")
    parser.add_argument("--overwrite_values", type=bool, default=False, help="Overwrite values")

    args = parser.parse_args()

    # Validate the token
    if not args.token:
        print("Please provide Alation API token either through --token option or ALATION_TOKEN environment variable.")
        sys.exit(1)

    # Validate the file path
    if not os.path.exists(args.file_path) or not os.path.isfile(args.file_path):
        print(f"The file path '{args.file_path}' does not exist or is not a file.")
        sys.exit(1)

    # Upload CSV and check job status
    task_id = upload_csv(args.alation_domain, args.object_type, args.object_id, args.file_path, args.token, args.overwrite_values)
    if task_id:
        check_job_status(args.alation_domain, task_id, args.token)

if __name__ == "__main__":
    main()