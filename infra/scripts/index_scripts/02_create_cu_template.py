# Import required modules


from azure.keyvault.secrets import SecretClient  
from azure.identity import DefaultAzureCredential
import sys
from pathlib import Path
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

key_vault_name = 'kv_to-be-replaced'

def get_secrets_from_kv(kv_name, secret_name):

    # Set the name of the Azure Key Vault  
    key_vault_name = kv_name 
    credential = DefaultAzureCredential()

    # Create a secret client object using the credential and Key Vault name  
    secret_client =  SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)  

    # Retrieve the secret value  
    return(secret_client.get_secret(secret_name).value)


# Add the parent directory to the path to use shared modules
parent_dir = Path(Path.cwd()).parent
sys.path.append(str(parent_dir))
from content_understanding_client import AzureContentUnderstandingClient
AZURE_AI_ENDPOINT = get_secrets_from_kv(key_vault_name,"AZURE-OPENAI-CU-ENDPOINT")
AZURE_AI_API_VERSION = "2024-12-01-preview" 


credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_ENDPOINT,
    api_version=AZURE_AI_API_VERSION,
    token_provider=token_provider
)


ANALYZER_ID = "ckm-4"
ANALYZER_TEMPLATE_FILE = '../../data/ckm-analyzer_config_text.json'


# Create analyzer
response = client.begin_create_analyzer(ANALYZER_ID, analyzer_template_path=ANALYZER_TEMPLATE_FILE)
result = client.poll_result(response)
























# endpoint = get_secrets_from_kv(key_vault_name,"AZURE-OPENAI-CU-ENDPOINT")
# api_key = get_secrets_from_kv(key_vault_name,"AZURE-OPENAI-CU-KEY")

# def create_cu_tempalte():
#     # Set content understanding service settings
#     AISERVICE_ENDPOINT = endpoint
#     API_KEY = api_key
#     API_VERSION = "?api-version=2024-12-01-preview"

#     # Set Content Understanding management api paths
#     PATH_ANALYZER_MANAGEMENT_ALL = "/contentunderstanding/analyzers"
#     PATH_ANALYZER_MANAGEMENT = "/contentunderstanding/analyzers/{analyzerId}"
#     PATH_ANALYZER_MANAGEMENT_OPERATION = "/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}"

#     # Set Content Understanding inference paths
#     PATH_ANALYZER_INFERENCE = "/contentunderstanding/analyzers/{analyzerId}:analyze"
#     PATH_ANALYZER_INFERENCE_GET_IMAGE = "/contentunderstanding/analyzers/{analyzerId}/results/{operationId}/images/{imageId}"


#     # helper method to poll for inferencing results
#     def poll_for_results(operation_location: str, success_state: str, failed_state: str, timeout: int = 300, interval: int = 2):
#         """
#         Polls the operation location URL until the operation reaches a success or failure state.

#         Args:
#             operation_location (str): The URL to poll for the operation result.
#             success_state (str): The status indicating the operation succeeded.
#             failed_state (str): The status indicating the operation failed.
#             timeout (int, optional): Maximum time to wait in seconds. Default is 60 seconds.
#             interval (int, optional): Time between polling attempts in seconds. Default is 2 seconds.

#         Returns:
#             dict or None: The final JSON response if successful, None otherwise.
#         """
#         headers = {
#             'Ocp-Apim-Subscription-Key': API_KEY,
#             'cogsvc-videoanalysis-face-identification-enable': "true"
#         }

#         # print(f'GET {operation_location}')

#         elapsed_time = 0
#         while elapsed_time <= timeout:
#             try:
#                 response = requests.get(operation_location, headers=headers)
#                 response.raise_for_status()
#                 result = response.json()
#                 # print(response)
#                 # print(result)

#                 status = result.get('status')
#                 if status == success_state:
#                     return result
#                 elif status == failed_state:
#                     print(f"Operation failed with status: {status}")
#                     return None

#                 time.sleep(interval)
#                 elapsed_time += interval

#             except requests.exceptions.RequestException as e:
#                 print(f"An error occurred: {e}")
#                 return None

#         print("Operation timed out.")
#         return None

#     def listAllfilesinPath(directory) -> List[str]:
#         return [join(directory, f) for f in listdir(directory) if (isfile(join(directory, f)) and not f.endswith('.json'))]

#     def loadAnalyzerfromFile(path, analyzer_name) -> dict:
#         with open(path) as json_file:
#             analyzer = json.load(json_file)
#         analyzer['analyzerId'] = analyzer_name
#         return analyzer


#     # helper method to create an analyzer
#     def create_analyzer(analyzer_config: str):
#         print(f"Creating analyzer with id: {analyzer_config['analyzerId']}")
#         headers = {
#             'Ocp-Apim-Subscription-Key': API_KEY,
#             'Content-Type': 'application/json',
#             'cogsvc-videoanalysis-face-identification-enable': "true"
#         }
#         print(f"PUT {AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzer_config['analyzerId'])}")
#         response = requests.put(AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzer_config["analyzerId"]) + API_VERSION, headers=headers, json=analyzer_config)
#         if ('apim-request-id' in response.headers):
#             print(f"request-id: {response.headers['apim-request-id']}")
#         print(response)
#         if response.status_code == 201:
#             final_state = poll_for_results(response.headers['Operation-Location'], 'Succeeded', 'Failed')
#         else:
#             final_state = response.json()
#             print(final_state)
        
#     # helper method to delete an analyzer
#     def delete_analyzer(analyzer_config: str):
#         headers = {
#             'Ocp-Apim-Subscription-Key': API_KEY,
#             'Content-Type': 'application/json',
#             'cogsvc-videoanalysis-face-identification-enable': "true"
#         }
#         print(f"DELETE {AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzer_config['analyzerId'])}")
        
#         response = requests.delete(AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzer_config["analyzerId"]) + API_VERSION, headers=headers)
#         if ('apim-request-id' in response.headers):
#             print(f"request-id: {response.headers['apim-request-id']}")
#         print(response)

#     # helper method to patch (update) an analyzer
#     def patch_analyzer(analyzer_config: str):
#         headers = {
#             'Ocp-Apim-Subscription-Key': API_KEY,
#             'Content-Type': 'application/json',
#             'cogsvc-videoanalysis-face-identification-enable': "true"
#         }
        
#         print(f"PATCH {AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzer_config['analyzerId'])}")
        
#         response = requests.patch(AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzer_config["analyzerId"]) + API_VERSION, headers=headers)
#         if ('apim-request-id' in response.headers):
#             print(f"request-id: {response.headers['apim-request-id']}")
#         print(response)
        
#     # helper method to list all analyzers
#     def list_all_analyzer():
#         headers = {
#             'Ocp-Apim-Subscription-Key': API_KEY
#         }

#         response = requests.get(AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT_ALL + API_VERSION , headers=headers)
#         return response.json()

#     # helper method to list all analyzers
#     def list_analyzer(analyzerId):
#         headers = {
#             'Ocp-Apim-Subscription-Key': API_KEY
#         }

#         response = requests.get(AISERVICE_ENDPOINT + PATH_ANALYZER_MANAGEMENT.format(analyzerId=analyzerId) + API_VERSION, headers=headers)
#         return response.json()


#     # Load an Analyzer from a file
#     mmi_analyzer_file = loadAnalyzerfromFile("./data/ckm-analyzer_config.json", "ckm-analyzer")

#     # delete any existing analyzers
#     analyzers = list_all_analyzer()
#     # print(analyzers['value'])
#     for analyzer in analyzers['value']:
#         if analyzer.get('analyzerId').startswith('prebuilt'):
#             continue
#         print(analyzer.get('analyzerId'))
#         delete_result = delete_analyzer(analyzer)
#         print(delete_result)


#     if mmi_analyzer_file == None:
#         print("Skipping. Please set the analyzer_name.")
#     else:
#         # Get timestamp and create output folder
#         timestamp = time.strftime("%Y%m%d-%H%M%S")

#         if "baseAnalyzerId" in mmi_analyzer_file:
#             print("ERROR: Base Analyzer config found!")
#             exit(0)
#         else:
#             print("Creating analyzer...")
#             create_analyzer(mmi_analyzer_file)		

# create_cu_tempalte()