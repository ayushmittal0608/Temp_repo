from azure.identity import ClientSecretCredentials
from azure.mgmt.costmanagement import CostManagementClient
import requests
import azure_credentials as az
import json

credentials = ClientSecretCredentials(
    client_id = az.client_id,
    client_secret = az.client_secret,
    tenant_id = az.tenant_id
)

token = credentials.get_token("https://management.azure.com/.default")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

subscription_id = az.subscription_id
scope = f"/subscriptions/{subscription_id}"
api_version = "2025-03-01"

url=f"https://management.azure.com{scope}/providers/Microsoft.CostManagement/anomalies?api-version={api_version}"

response = requests.get(url, headers=headers)

if response.status_code==200:
    recommendations = response.json().get("value", [])
    cost_recommendations = []
    for rec in recommendations:
        category = rec["properties"].get("category")
        if category=="Cost":
            cost_recommendations.append({
                "recommendation": rec["properties"].get("shortDescription", {}).get("problem"),
                "impact": rec["properties"].get("impact"),
                "resource": rec["properties"].get("impactedField") + "=" + rec["properties"],
                "action": rec["properties"].get("shortDescription", {}).get("solution")
            })
    print(json.dumps(cost_recommendations, indent=4))
    
else:
    print(response.text)
