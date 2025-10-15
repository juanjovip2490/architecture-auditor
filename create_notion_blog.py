import requests
import json

# Notion API configuration
NOTION_TOKEN = "ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U"
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

# First, search for the "analyst" page
search_payload = {
    "query": "analyst",
    "filter": {"property": "object", "value": "page"}
}

search_response = requests.post(
    "https://api.notion.com/v1/search",
    headers=headers,
    json=search_payload
)

if search_response.status_code == 200:
    results = search_response.json().get("results", [])
    analyst_page = next((page for page in results if page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "").lower() == "analyst"), None)
    
    if analyst_page:
        parent_id = analyst_page["id"]
        
        # Create the "Project Analysis" blog page
        create_payload = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": "Project Analysis"}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"text": {"content": "Project Analysis"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": "This is a detailed analysis of the current project status, objectives, and outcomes."}}]}
                }
            ]
        }
        
        create_response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=create_payload
        )
        
        if create_response.status_code == 200:
            print("Successfully created 'Project Analysis' page in analyst workspace")
        else:
            print(f"Error creating page: {create_response.text}")
    else:
        print("Could not find 'analyst' page")
else:
    print(f"Error searching for analyst page: {search_response.text}")