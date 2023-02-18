# Orca API Wrapper Script

Refer to Orca documenation [here](https://docs.orcasecurity.io/docs/detailed-query-api-examples) for further details and the latest version of this script.

- [Orca API Wrapper Script](#orca-api-wrapper-script)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Ensure Location is Set Correctly](#ensure-location-is-set-correctly)
  - [Examples](#examples)
    - [Querying with email and password](#querying-with-email-and-password)
    - [Querying with API token](#querying-with-api-token)
    - [Returning resolved alerts](#returning-resolved-alerts)
      - [Usage](#usage-1)
    - [Returning data in csv format](#returning-data-in-csv-format)
      - [Examples](#examples-1)
        - [Export all alerts to CSV:](#export-all-alerts-to-csv)
        - [Export all vulnerabilities to CSV:](#export-all-vulnerabilities-to-csv)
    - [Getting help](#getting-help)


## Requirements

- Python 3.x
- `argparse`, `json`, `requests` libraries

## Usage

To use the script, run the following command:

`
python3 orca_api_wrapper.py [--api-url API_URL] [--email EMAIL --password PASSWORD | --api-token API_TOKEN] --query-type QUERY_TYPE (--output-json-file OUTPUT_JSON_FILE | --output-download-link) [query_params [query_params ...]]
`


- `--api-url API_URL` (optional): the endpoint to connect to. Default is `https://app.us.orcasecurity.io/api`.
- `--email EMAIL` (optional): your user email address.
- `--password PASSWORD` (optional): your user password.
- `--api-token API_TOKEN` (optional): your API token.
- `--query-type QUERY_TYPE` (required): the data set to query.
- `--output-json-file OUTPUT_JSON_FILE` (optional): the name of the output file.
- `--output-download-link` (optional): get output as a downloadable link.
- `query_params` (optional): the parameters for the query.

You must specify either `--output-json-file` or `--output-download-link`.

If using email/password authentication, you must specify `--email` and `--password`. If using API token authentication, you must specify `--api-token`.

## Ensure Location is Set Correctly
By Default the --api-url flag is set to the US region "https://app.us.orcasecurity.io/api"

In case you are using a different region, use the --api-url flag in the command to update your region:

EU
`
--api-url "https://app.eu.orcasecurity.io/api"
`

AU
`
--api-url "https://app.au.orcasecurity.io/api"
`

IND
`
--api-url "https://app.in.orcasecurity.io/api"
`

GOV
`
--api-url "https://app.us-gov.orcasecurity.io/api"
`

## Examples

### Querying with email and password

To query with email and password authentication and output the results to a file, run:

`
python3 orca_api_wrapper.py --email example@example.com --password example_password --query-type example_query --output-json-file output.json param1 value1 param2 value2
`


### Querying with API token

To query with API token authentication and output the results as a downloadable link, run:

`
python3 orca_api_wrapper.py --api-token EXAMPLE_API_TOKEN --query-type example_query --output-download-link param1 value1 param2 value2
`

`
python3 orca_api_wrapper.py --api-url "https://app.au.orcasecurity.io/api" --api-token EXAMPLE_API_TOKEN --query-type alerts --output-json-file alerts.json 
`

### Returning resolved alerts

Resolved alerts are defined as:

- alerts moved to status closed, done, dismissed.
- alerts that change score from 1-3 to 4

#### Usage
Resolved alerts can be obtained using one of two parameters:


| Parameter	            | Type	    | Description |
|---|---|---|
| resolved_alerts	    | Boolean	| All resolved alerts in the last 30 days |
| resolved_alerts_days	| int	    | Will return resolved alerts in the last X specified days |

Examples
Below are usage examples for both use cases.

Obtain all resolved alerts and output to resolved_alerts.json file:

`
orca_api_wrapper.py --api-url "https://app.au.orcasecurity.io/api" --api-token EXAMPLE_API_TOKEN --query-type alerts --output-json-file resolved_alerts.json-- resolved_alerts true
`
### Returning data in csv format

You can use the --output-download-link and --csv_delimiter parameters to return data in csv format

#### Examples

##### Export all alerts to CSV:

`
orca_api_wrapper.py --api-url "https://app.au.orcasecurity.io/api" --api-token EXAMPLE_API_TOKEN --query-type alerts --output-download-link --csv_delimiter ";"
`

##### Export all vulnerabilities to CSV:

`
orca_api_wrapper.py --api-url "https://app.au.orcasecurity.io/api" --api-token EXAMPLE_API_TOKEN --query-type alerts --output-download-link --csv_delimiter ";"
`

### Getting help

To get help on the script, run:

`
python cloud_account_query.py -h
`
