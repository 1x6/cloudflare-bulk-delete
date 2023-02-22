import concurrent.futures
from typing import Dict

import requests


def get_zone_id(domain: str, headers: Dict[str, str]) -> str:
    """Retrieves the ID for the Cloudflare zone associated with the given domain.

    params:
        domain: A string representing the domain name.
        headers: A dictionary containing the Cloudflare API authentication headers.

    returns:
        A string representing the ID of the Cloudflare zone associated with the given domain.
    """
    response = requests.get(
        f'https://api.cloudflare.com/client/v4/zones?name={domain}',
        headers=headers,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()['result'][0]['id']


def delete_dns_record(
    record_id: str, dns_url: str, headers: Dict[str, str]
) -> None:
    """Deletes a DNS record with the specified ID.

    params:
        record_id: A string representing the ID of the DNS record to delete.
        dns_url: A string representing the URL of the Cloudflare DNS records API.
        headers: A dictionary containing the Cloudflare API authentication headers.

    returns:
        None
    """
    response = requests.delete(
        f'{dns_url}/{record_id}', headers=headers, timeout=5
    )
    response.raise_for_status()
    print(response.text)


def main() -> None:
    """Deletes all DNS records for a given domain using the Cloudflare API.

    Prompts the user for Cloudflare API authentication credentials and the domain name, then retrieves the ID for the
    associated Cloudflare zone and the list of DNS records for the domain. Uses a ThreadPoolExecutor to submit delete
    requests for each DNS record and print the response.

    returns:
        None
    """
    email = input('Email: ')
    api_key = input('API Key: ')
    domain = input('Domain: ')
    headers = {'X-Auth-Email': email, 'X-Auth-Key': api_key}

    zone_id = get_zone_id(domain, headers)
    dns_url = (
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    )

    response = requests.get(dns_url, headers=headers, timeout=5)
    response.raise_for_status()
    records = response.json()['result']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(delete_dns_record, record['id'], dns_url, headers)
            for record in records
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except requests.exceptions.HTTPError as error:
                print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
