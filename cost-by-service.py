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
        "name": "ServiceName"
    }
}

cost_client = CostManagementClient(credential)
result = cost_client.query.usage(scope=scope, parameters=query)

for row in result.rows:
    service_costs = [
        {
            "service": row[0],
            "cost": float(row[1])
        }
    ]
    
print(json.dumps(service_costs, indent=4))
