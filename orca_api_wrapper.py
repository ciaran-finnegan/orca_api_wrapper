import argparse    # for parsing command line arguments
import json        # for working with JSON data
import requests    # for making HTTP requests
import time        # for time-related operations

# function to perform user authentication and return an access token
def login(api_url, email=None, password=None):
    """
    :param api_url: the URL of the API endpoint
    :param email: the user email address (required if password is provided)
    :param password: the user password (required if email is provided)
    :return: the access token for the authenticated user
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


# function to query the cloud account and either get a download link or save the results to a file
def query(api_url, jwt_token, api_token, query_type, output_file, query_param_list):
    """
    :param api_url: the URL of the API endpoint
    :param jwt_token: the access token for the authenticated user (if using email/password authentication)
    :param api_token: the API token for the cloud account (if using API token authentication)
    :param query_type: the type of query to make (e.g. "alerts", "hosts", "events", etc.)
    :param output_file: the name of the output file to save the query results to (if provided)
    :param query_param_list: a list of query parameters (specified as key-value pairs)
    """
    # set the appropriate authentication header based on the provided token
    if jwt_token:
        auth_header = {"Authorization": f"Bearer {jwt_token}"}
    else:
        auth_header = {"Authorization": f"Token {api_token}"}

    url = f"{api_url}/query/{query_type}"

    params = {}

    # check if the query parameters list has an even length (since parameters are specified as key-value pairs)
    num_params = len(query_param_list)
    if num_params % 2 != 0:
        print(
            f"got query parameters: {' '.join(query_param_list)}, but expecting even length list: key1 value2 key2 value2..."
        )
        return

    # convert the query parameters list into a dictionary
    for index in range(num_params // 2):
        params[query_param_list[index * 2]] = query_param_list[index * 2 + 1]

    # if output_file is specified, chunk the data into 500-item pieces and save to a JSON file
    if output_file:
        params["limit"] = 500  # chunk size, can be between 1 and 1000

        data = None

        # get a chunk of data in each API call and loop until all items are retrieved
        while True:
            # make the API call and get the response data as a JSON object
            res = requests.get(url, headers=auth_header, params=params).json()

            if res["status"] != "success":
                print(f'getting items for {query_type} failed, params: {params}, error: {res["error"]}')
                return

            # if the response data is a list, append it to the data array (if it exists), else assign it to data
            if type(res["data"]) == list:
                if not data:
                    data = []
               
