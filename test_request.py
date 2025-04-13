import requests
import json

url = "http://localhost:8080/v1/scrap"
data = {
    "url": "https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/protsessory-ASgBAgICAkTGB~pm7gniZw?cd=1&q=i5+12400f"
}

print(f"Sending request to: {url}")
print(f"Request data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"\nStatus code: {response.status_code}")
    print(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
    print(f"\nResponse text preview: {response.text[:500]}")
except requests.exceptions.RequestException as e:
    print(f"\nError occurred: {str(e)}") 