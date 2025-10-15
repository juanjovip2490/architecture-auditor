import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": "Bearer ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Search for all pages
search = requests.post("https://api.notion.com/v1/search", headers=headers, json={}, verify=False)

if search.status_code == 200:
    results = search.json().get("results", [])
    print(f"Found {len(results)} pages:")
    for page in results:
        title = ""
        if page.get("properties", {}).get("title", {}).get("title"):
            title = page["properties"]["title"]["title"][0].get("plain_text", "")
        elif page.get("properties", {}).get("Name", {}).get("title"):
            title = page["properties"]["Name"]["title"][0].get("plain_text", "")
        print(f"- {title} (ID: {page['id']})")
else:
    print(f"Error: {search.text}")