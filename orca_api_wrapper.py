import argparse    # module for parsing command-line arguments
import json        # module for working with JSON data
import requests    # module for sending HTTP requests
import time        # module for working with time

def login(api_url, email=None, password=None):
    """
    Log in to the cloud account and retrieve a JSON Web Token (JWT).
    
    Parameters:
    - api_url: str, the API endpoint to connect to.
    - email: str (optional), the user email address.
    - password: str (optional), the user password.
    
    Returns:
    - str, the JWT access token.
    """
    
    url = f"{api_url}/user/session"

    data = {
         "email": email,
         "password": password,
    }

    resp = requests.post(url, data=data)
    
    if resp.status_code != 200:
        print("login failed, check the credentials")
        exit(0)

    return resp.json()["jwt"]["access"]

def query(api_url, jwt_token, api_token, query_type, output_file, query_param_list):
    """
    Query the cloud account and either save the results to a JSON file or retrieve a downloadable link to the results.
    
    Parameters:
    - api_url: str, the API endpoint to connect to.
    - jwt_token: str (optional), the JWT access token.
    - api_token: str (optional), the API token.
    - query_type: str, the type of data set to query.
    - output_file: str (optional), the name of the output file to save the results.
    - query_param_list: list of str, the list of query parameters.
    
    Returns:
    - None.
    """
    
    if jwt_token:
        auth_header = {"Authorization": f"Bearer {jwt_token}"}
    else:
        auth_header = {"Authorization": f"Token {api_token}"}

    url = f"{api_url}/query/{query_type}"

    params = {}

    num_params = len(query_param_list)
    
    if num_params % 2 != 0:
        print(f"got query parameters: {' '.join(query_param_list)}, but expecting even length list: key1 value2 key2 value2...")
        return

    for index in range(num_params // 2):
        params[query_param_list[index * 2]] = query_param_list[index * 2 + 1]

    if output_file:
        params["limit"] = 500  # chunk size, can be between 1 and 1000

        data = None

        # we get chunk of data in each api call, loop until we got all items
        while True:
            # do the api call
            res = requests.get(url, headers=auth_header, params=params).json()

            if res["status"] != "success":
                print(f'getting items for {query_type} failed, params: {params}, error: {res["error"]}')
                return

            if type(res["data"]) == list:
                if not data:
                    data = []
                data += res["data"]
                print(f"got {len(data)}/{res['total_items']} {query_type}")
            else:
                data = res["data"]

            if "next_page_token" not in res:
                # that was the last chunk
                break

            # pass this token in the next call to get the next chunk
            params["next_page_token"] = res["next_page_token"]

        print(f"writing {len(data)} {query_type} to {output_file}")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
    else:
        params["get_download_link"] = True  # get link to dowdload all results
        params["download_async"] = True

        res = requests.get(url, headers=auth_header, params=params).json()

        if res["status"] != "success":
            print(f'getting items for {query_type} failed, params: {params}, error: {res["error"]}') 
            return

        request_token = res["request_token"]
        url_status = f"{api_url}/query/status/"
        while True:
            res = requests.get(url_status, headers=auth_header, params={"request_token": request_token}).json()
            if res["query_status"] == "success":
                print(f"download results from:\n{res['file_location']}")
                break
            print("waiting for results to be ready")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Query cloud account")
    parser.add_argument("--api-url", help="endpoint to connect to", default="https://app.us.orcasecurity.io/api")
    parser.add_argument("--email", help="User email address")
    parser.add_argument("--password", help="The user password")
    parser.add_argument("--api-token", help="API token")
    parser.add_argument("--query-type", help="The data set to query", required=True)
    parser.add_argument("--output-json-file", help="name of output file")
    parser.add_argument(
        "--output-download-link", action="store_true", default=False, help="get output as downloadble link"
    )
    parser.add_argument("query_params", help="parameters for the query", nargs="*")

    args = parser.parse_args()

    if not args.output_json_file and not args.output_download_link:
        print("need to specify either --output-json-file or --output-download-link")
        return

    if not (args.email and args.password) and not args.api_token:
        print("need to specify email/password or api_token")
        return

    if args.email and args.password:
        # email password auth
        jwt_token = login(args.api_url, email=args.email, password=args.password)
        query(args.api_url, jwt_token, None, args.query_type, args.output_json_file, args.query_params)
    else:
        query(args.api_url, None, args.api_token, args.query_type, args.output_json_file, args.query_params)


if __name__ == "__main__":
    main()