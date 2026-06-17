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
    
    from log_fetcher.utils.exceptions import AuthenticationException, UpstreamAPIException

    try:
        response = requests.post(
            url,
            headers=headers,
            json=graphql_query,
            timeout=30
        )
        
        if response.status_code in (401, 403):
            raise AuthenticationException("Invalid or unauthorized New Relic API Key")
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        raise UpstreamAPIException("New Relic API request timed out")
    except requests.exceptions.RequestException as e:
        raise UpstreamAPIException(f"Failed to communicate with New Relic API: {str(e)}")