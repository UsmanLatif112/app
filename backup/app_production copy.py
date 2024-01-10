from flask import Flask, render_template, request, jsonify
import csv, json
import time
import requests
from csv import reader

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/script')
def script():
    return render_template('script.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    # Retrieve the campaign_id from the form data
    campaign_idd = request.form.get('campaign_id')

    # http://69.167.136.19:8010
    Piroty_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBaW1hbFJhemEiLCJUT0tFTiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUp6ZFdJaU9pSkJhVzFoYkZKaGVtRWlMQ0p6WTI5d1pYTWlPbHRkTENKcFpDSTZOVEF4TENKbGVIQWlPakUzTURZeU5qWTBNalI5LjNBZDBpZHJpU2hBNnBseV81cUZJR3pweHo0VERnUlFkNTgwZ1RrU2RyTkkiLCJleHAiOjIwMTk0NjY0MjR9.n6JnySi-gZvrbpxO0kQOlb0hxmNQwhmHsW9aOq_PBXY"
    # id = "19233"
    id = f'{campaign_idd}'
    # ================================================

    # Campaign ID which is deleted in first in delete api and get single campaign data with campaign id.

    Campaign_ID = f"{id}"

    # Campaign IDd which is used for other apis in which we need campaign id to get data
    # (Dont Delete Cam1)

    Campaign_IDd = "18299" 

    # Campaign IDdd which is used to add 8th keyword in campaign already having 7 keywords
    # (Dont Delete Cam2)

    Campaign_IDdd = "18268"

    # Campaign IDdr which is used to delete last keyword of campaign
    # (Dont Delete Cam3)

    Campaign_IDdr = "18414"

    # Campaign IDdt which is used to deauthorize business.
    # (Business campaign Del 4)

    Campaign_IDdt = "18301"

    # Client id is used to get client api

    Client_id = "1196"

    # Keyword which is used to create keyword add keyword or delete keyword

    Keyword_new = f"apimusthave{id}"

    # Client name which is used to create new client

    Client_Name_New = f"apimusthave{id}"

    # ================================================

    # data which is used to create new campaign

    business_gmb_CID = "10469100432931003566"
    Campaign_name = f"Apimusthave{id}"
    Client_name = "APITEST0026"
    keywords_for_analysis = "Red Royal Electric,American restaurant"

    # ========================
    api_list = []
    # ======================================
    auth_token = Piroty_token
    # ======================================
    # Add a dictionary to store custom error messages for specific response codes
    custom_error_messages = {
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authentication Required',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        418: 'iam',
        421: 'Misdirected Request',
        422: 'Unprocessable Entity',
        423: 'Locked',
        424: 'Failed Dependency',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        431: 'Request Header Fields Too Large',
        451: 'Unavailable For Legal Reasons',
        429: 'Too Many Requests',
    }
    # ================================================

    # Initialize the response codes dictionary
    response_codes_dict = {}

    # Function to hit the APIs and save results in a CSV file
    def hit_apis_and_save_results(api_list, auth_token, csv_filename):
        # with open(csv_filename, 'w', newline='') as csvfile:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # writer = csv.writer(csvfile)
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(['Description','API', 'Method', 'Response Code', 'Result (according to response code)', 'Response Time', 'Response Message', 'Response Data', 'Response Data Result'])
            # writer.writerow(['\n'])

            # Iterate over each API in the list
            for api in api_list:
                description = api.get('description', 'No description provided')
                url = api['url']
                method = api['method']
                params = api['params']

                headers = {
                    'Authorization': f'Bearer {auth_token}',
                    'Content-Type': 'application/json'
                }

                try:
                    # Print the API description
                    print("==============================================")
                    print("   ")
                    print(f"API Description: {description}")

                    # Make the API request
                    start_time = time.time()
                    
                    response = requests.request(method, url, json=params, headers=headers)
                    response_code = response.status_code
                    response_time = time.time() - start_time

                    response_message = custom_error_messages.get(response_code, '')
                    response_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text

                    # Determine the result based on response data
                    if response_data == {'items': [], 'total': 0, 'page': 1, 'size': 50}:
                        response_result = "Fail"
                    else:
                        response_result = "Pass"

                    result_according_to_response_code = "Pass" if response_code in [200, 201, 202] else "Fail"
                    # Write the results to the CSV file
                    # writer.writerow([description])
                    # writer.writerow([url, method, response_code, result_according_to_response_code, response_time, response_message, response_data, response_result])
                    # writer.writerow(['\n'])
                    response_data = str(response_data).replace('"', ';')
                    
                    writer.writerow([description, url, method, response_code, result_according_to_response_code, response_time, response_message,f'"{response_data}"', response_result])  
                    
                    # Print the results in the terminal
                    print(f"API: {url}, Method: {method}, Response Code: {response_code}, Result (according to response code): {result_according_to_response_code}, "
                        f"Response Time: {response_time:.2f}, Response Message: {response_message}, Response Data: {response_data}, Response Data Result: {response_result}")

                    # Wait for 1 second before the next API hit
                    time.sleep(1)

                except Exception as e:
                    print("==============================================")
                    print("   ")
                    print(f"Error occurred while processing API: {url}, Method: {method}, Error: {e}")

            print("==============================================")
            print("   ")
            print("API hits completed.")

    # Call the function to hit the APIs and save the results
    hit_apis_and_save_results(api_list, auth_token, 'API_result.csv')
    
    # =====================================================================================
    # For example, let's assume your script's function is `hit_apis_and_save_results`
    auth_token = Piroty_token
    api_list = [
         # ====//// == Agency API == ////=======
    
            # {
            #     "description": "Create campaign with correct data",
            #     "url": "http://69.167.136.19:8010/campaigns/create/",
            #     "method": "POST",
            #     "params":
            #         {
            #         "business_gmb_cid": business_gmb_CID,
            #         "campaign_name": Campaign_name,
            #         "client_name": Client_name,
            #         "keywords_for_analysis": keywords_for_analysis
            #         }
            # },
            
            # {
            #     "description": "Create campaign with incorrect GMB CID",
            #     "url": "http://69.167.136.19:8010/campaigns/create/",
            #     "method": "POST",
            #     "params":
            #         {
            #         "business_gmb_cid": "98649953187944340729864995318",
            #         "campaign_name": Campaign_name,
            #         "client_name": Client_name,
            #         "keywords_for_analysis": keywords_for_analysis
            #         }
            # },
            
            # # =============================================================
            
            {
                "description": "Get campaign by providing campaign ID",
                "url": f"http://69.167.136.19:8010/campaigns/{Campaign_ID}/",
                "method": "GET",
                "params": None
            },
            {
                "description": "Get campaign by providing incorrect campaign ID",
                "url": "http://69.167.136.19:8010/campaigns/177/",
                "method": "GET",
                "params": None
            },
            
            # # =============================================================
            
            {
                "description": "Get list of all campaigns",
                "url": "http://69.167.136.19:8010/campaigns/list/all/",
                "method": "GET",
                "params": None
            },
            
            # # =============================================================
            
            {
                "description": "Delete campaign by providing campaign ID",
                "url": f"http://69.167.136.19:8010/campaigns/delete/{Campaign_ID}/",
                "method": "DELETE",
                "params": None
            },
            
            {
                "description": "Delete campaign by providing incorrect campaign ID",
                "url": f"http://69.167.136.19:8010/campaigns/delete/1289/",
                "method": "DELETE",
                "params": None
            },
            
            # {
            #     "description": "Delete campaign by providing already deleted campaign ID",
            #     "url": f"http://69.167.136.19:8010/campaigns/delete/{Campaign_ID}/",
            #     "method": "DELETE",
            #     "params": None
            # },
            
            # # =============================================================
            
            {
                "description": "Create Client",
                "url": "http://69.167.136.19:8010/clients/create/",
                "method": "POST",
                "params":
                    {
                        "client_name": Client_Name_New
                        }
            },
            {
                "description": "Create client with already created client name",
                "url": "http://69.167.136.19:8010/clients/create/",
                "method": "POST",
                "params":
                    {
                        "client_name": Client_Name_New
                        }
            },
            
            # # ======================================
            
            {
                "description": "Get client by providing client ID",
                "url": f"http://69.167.136.19:8010/clients/{Client_id}/",
                "method": "GET",
                "params": None
            },
            {
                "description": "Get client by providing incorrect client ID",
                "url": f"http://69.167.136.19:8010/clients/128/",
                "method": "GET",
                "params": None
            },
            
            # # # ======================================
            
            {
                "description": "Get list of all clients",
                "url": f"http://69.167.136.19:8010/clients/clients/list/",
                "method": "GET",
                "params": None
            },
            
            # # ======================================
            
            {
                "description": "Get list of all Geo Gifs URLs",
                "url": "http://69.167.136.19:8010/geo/gifs/urls/list/",
                "method": "GET",
                "params":
                    {
                    "Page": 1,
                    "Size": 50
                    }   
            },
            
            # # ======================================
            
            {
                "description": "Get list of Geo Gifs URLs by providing campaign ID",
                "url": f"http://69.167.136.19:8010/geo/gifs/urls/campaign/{Campaign_IDd}",
                "method": "GET",
                "params": None
            },
            {
                "description": "Get list of Geo Gifs URLs by providing incorrect campaign ID",
                "url": f"http://69.167.136.19:8010/geo/gifs/urls/campaign/1205",
                "method": "GET",
                "params": None
            },
            
            # # ======================================
            
            # {
            #     "description": "Get list of all Geo Grids URLs",
            #     "url": "http://69.167.136.19:8010/geo/grid/urls/list/all/",
            #     "method": "GET",
            #     "params": None
            # },
            
            # # ======================================
            
            {
                "description": "Get list of Geo Grids URLs by providing campaign ID",
                "url": f"http://69.167.136.19:8010/geo/grid/urls/{Campaign_IDd}/",
                "method": "GET",
                "params": None
            },
            
            {
                "description": "Get list of Geo Grids URLs by providing incorrect campaign ID",
                "url": f"http://69.167.136.19:8010/geo/grid/urls/1496/",
                "method": "GET",
                "params": None
            },
            
            # # ======================================
            
            # {
            #     "description": "Get list of latest Grids URLs by providing campaign ID",
            #     "url": f"http://69.167.136.19:8010/geo/grid/urls/latest/{Campaign_IDd}",
            #     "method": "GET",
            #     "params": None
            # },
            
            # {
            #     "description": "Get list of latest Grids URLs by providing incorrect campaign ID",
            #     "url": f"http://69.167.136.19:8010/geo/grid/urls/latest/8573",
            #     "method": "GET",
            #     "params": None
            # },
            
            # # ======================================
            
            # {
            #     "description": "Add keyword in campaign by providing campaign id",
            #     "url": "http://69.167.136.19:8010/keyword/create/",
            #     "method": "POST",
            #     "params":
            #         {
            #         "campaign_id": Campaign_IDd,
            #         "keyword": Keyword_new
            #         }
            # },
            # {
            #     "description": "Add keyword which is already added in campaign by providing campaign id",
            #     "url": "http://69.167.136.19:8010/keyword/create/",
            #     "method": "POST",
            #     "params":
            #         {
            #         "campaign_id": Campaign_IDd,
            #         "keyword": Keyword_new
            #         }
            # },
            # {
            #     "description": "Add keyword in campaign already having 7 keywords by providing campaign id",
            #     "url": "http://69.167.136.19:8010/keyword/create/",
            #     "method": "POST",
            #     "params":
            #         {
            #         "campaign_id": Campaign_IDdd,
            #         "keyword": "Pathan12323"
            #         }
            # },
            
            # # ======================================
            
            # {
            #     "description": "Delete keyword from campaign by providing campaign ID",
            #     "url": f"http://69.167.136.19:8010/keyword/delete/{Keyword_new}/{Campaign_IDd}",
            #     "method": "DELETE",
            #     "params": None
            # },
            # {
            #     "description": "Delete keyword which is already deleted from campaign by providing campaign ID",
            #     "url": f"http://69.167.136.19:8010/keyword/delete/{Keyword_new}/{Campaign_IDd}",
            #     "method": "DELETE",
            #     "params": None
            # },
            # {
            #     "description": "Try to delete last keyword of campaign by providing campaign ID",
            #     "url": f"http://69.167.136.19:8010/keyword/delete/ramen/{Campaign_IDdr}",
            #     "method": "DELETE",
            #     "params": None
            # },
            
            # # ======================================
            
            # {
            #     "description": "Deauthroize business by providing campaign ID",
            #     "url": f"http://69.167.136.19:8010/campaigns/business/deauthorization/{Campaign_IDdt}",
            #     "method": "GET",
            #     "params": None
            # },
            # {
            #     "description": "Deauthroize business which is already deauthroize by providing campaign ID",
            #     "url": f"http://69.167.136.19:8010/campaigns/business/deauthorization/{Campaign_IDdt}",
            #     "method": "GET",
            #     "params": None
            # },
            # {
            #     "description": "Deauthroize business by providing incorrect campaign ID",
            #     "url": f"http://69.167.136.19:8010/campaigns/business/deauthorization/{Campaign_IDdr}",
            #     "method": "GET",
            #     "params": None
            # },
            
            # # ======================================    
        ]  # Your API list

    # Call the function to hit the APIs and save the results
    result_file = 'API_result.csv'
    hit_apis_and_save_results(api_list, auth_token, result_file)

    # Read the CSV file and convert its content into a list of lists
    with open(result_file, 'r', encoding='utf-8') as file:
        result_content = list(reader(file))

    # Skip the header row (first row of the CSV)
    result_content = result_content[1:]

    # Return the data as JSON
    return jsonify(result_content)
    # return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)