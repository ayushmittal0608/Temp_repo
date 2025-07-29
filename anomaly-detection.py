import requests
import json
from azure.identity import ClientSecretCredentials
from azure.mgmt.costmanagement import CostManagementClient
import azure_credentials as az

credentials = ClientSecretCredentials(
    client_id = az.client_id,
    client_secret = az.client_secret,
    tenant_id = az.tenant_id
)

token = credentials.get_token("https://management.azure.com/.default").token

subscription_id = az.subscription_id
scope = f"/subscriptions/{subscription_id}"
api_version = "2025-03-01"

url=f"https://management.azure.com{scope}/providers/Microsoft.CostManagement/anomalies?api-version={api_version}"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
anomalies = response.json()

print(json.dumps(anomalies, indent=4))
