from azure.identity import ClientSecretCredentials
from azure.mgmt.costmanagement import CostManagementClient
from datetime import date
import json
import azure_credentials as az

credential = ClientSecretCredentials(
    client_id = az.client_id,
    client_secret = az.client_secret,
    tenant_id = az.tenant_id
)

subscription_id = az.subscription_id
scope = f"/subscriptions/{subscription_id}"

account_query = {
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
        "name": "ResourceGroupName"
    }
}

cost_client = CostManagementClient(credential)
result = cost_client.query.usage(scope=scope, parameters=account_query)

for row in result.rows:
    cost_by_account = [
        {
            "resource_group": row[0],
            "cost": float(row[1])
        }
    ]

print(json.dumps(cost_by_account, indent=4))

