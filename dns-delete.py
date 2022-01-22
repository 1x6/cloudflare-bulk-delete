import requests, threading

email = "xeny@esex.com"
api_key = "lolz"
headers = {"X-Auth-Email": email, "X-Auth-Key": api_key}

def get_zone_id(domain):
    gz = requests.get("https://api.cloudflare.com/client/v4/zones?name=" + domain, headers=headers).json()
    return gz["result"][0]["id"]

zone_id = get_zone_id("vast.lol")  # change this to ur domain
dns_url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/"

def delete(_id):
    delet = requests.delete(dns_url + _id, headers=headers)
    print(delet.text)

r = requests.get(dns_url, headers=headers).json()
for record in r["result"]:
    _id = record["id"]
    threading.Thread(target=delete, args=(_id,)).start()

