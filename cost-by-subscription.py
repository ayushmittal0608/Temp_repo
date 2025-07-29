from az.identity import ClientSecretCredentials
from az.mgmt.costmanagement import CostManagementClient
import azure_credentials as az
import json

credential = ClientSecretCredentials(
    client_id = az.client_id,
    client_secret = az.client_secret,
    tenant_id = az.tenant_id
)

subscription_id = az.subscription_id
scope = f"/subscriptions/{subscription_id}"

query = {
    "type": "Usage",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "None",
        "aggregation": {
            "name": "PreTaxCost",
            "function": "Sum"
        }
    },
    "grouping": {
        "type": "Dimension",
        "name": "SubscriptionName"
    }
}

cost_client = CostManagementClient(credential)
result = cost_client.query.usage(scope=scope, parameter=query)

for row in result.rows:
    subscription_cost = [
        {
            "subscriptionId": row[0],
            "cost": row[1]
        }
    ]
    
print(json.dumps(subscription_cost, indent=4))
