import requests

from log_fetcher.config.settings import (
    NEW_RELIC_USER_KEY,
    NEW_RELIC_ACCOUNT_ID
)


def fetch_logs(
    service_name,
    start_time,
    end_time,
    trace_id=None
):

    nrql_query = (
        f"SELECT * FROM Log "
        f"WHERE service = '{service_name}' "    
        f"SINCE {start_time} "
        f"UNTIL {end_time}"
    )

   

    url = "https://api.newrelic.com/graphql"

    headers = {
        "Content-Type": "application/json",
        "API-Key": NEW_RELIC_USER_KEY
    }

    graphql_query = {
        "query": f"""
        {{
          actor {{
            account(id: {NEW_RELIC_ACCOUNT_ID}) {{
              nrql(query: "{nrql_query}") {{
                results
              }}
            }}
          }}
        }}
        """
    }
    
    response = requests.post(
        url,
        headers=headers,
        json=graphql_query
    )

    return response.json()