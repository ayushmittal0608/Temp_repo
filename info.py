from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
from msgraph.core import GraphClient
from datetime import date
import json

import azure_credentials as az

credential = ClientSecretCredential(
    tenant_id = az.tenant_id,
    client_id = az.client_id,
    client_secret = az.client_secret
)

cost_client = CostManagementClient(credential)
subscription_id = az.subscription_id
scope = f"/subscriptions/{subscription_id}"

today = date.today()

actual_cost_query = {
    "type": "Usage",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "None",
        "aggregation": {
            "totalCost": {
                "name": "preTaxCost",
                "function": "Sum"
            }
        }
    }
}

forecast_cost_query = {
    "type": "Forecast",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "None",
        "aggregation": {
            "totalCost": {
                "name": "preTaxCost",
                "function": "Sum"
            }
        }
    }
}

actual_result = cost_client.query.usage(scope=scope, parameters=actual_cost_query)
forecast_result = cost_client.query.usage(scope=scope, parameters=forecast_cost_query)

actual_cost = float(actual_result.rows[0][0])
forecast_cost = float(forecast_result.rows[0][0])

resource_query = QueryRequest (
    subscriptions=[subscription_id],
    query="Resource | summarize count() by type"
)

graph_client = GraphClient(credential=credential)
result = graph_client.resources(resource_query)
total_services = len(result.data)

try:
    user_data = graph_client.get('/users?top=999')
    total_users = len(user_data.json().get('value', []))
except Exception as e:
    print(e)
    
info_list = {
    "actual_cost": actual_cost,
    "forecast_cost": forecast_cost,
    "total_services": total_services,
    "total_users": total_users
}

print(json.dumps(info_list, indent=4))
