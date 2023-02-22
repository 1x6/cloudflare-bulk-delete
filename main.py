import concurrent.futures
import requests
from typing import Dict, List


def get_zone_id(domain: str, headers: Dict[str, str]) -> str:
    response = requests.get(f'https://api.cloudflare.com/client/v4/zones?name={domain}', headers=headers)
    response.raise_for_status()
    return response.json()['result'][0]['id']


def delete_dns_record(record_id: str, dns_url: str, headers: Dict[str, str]) -> None:
    response = requests.delete(f'{dns_url}/{record_id}', headers=headers)
    response.raise_for_status()
    print(response.text)


def main() -> None:
    email = input('Email: ')
    api_key = input('API Key: ')
    domain = input('Domain: ')
    headers = {'X-Auth-Email': email, 'X-Auth-Key': api_key}

    zone_id = get_zone_id(domain, headers)
    dns_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    response = requests.get(dns_url, headers=headers)
    response.raise_for_status()
    records = response.json()['result']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(delete_dns_record, record['id'], dns_url, headers) for record in records]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except requests.exceptions.HTTPError as error:
                print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
