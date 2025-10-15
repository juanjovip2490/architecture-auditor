import requests

headers = {
    "Authorization": "Bearer ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Search for analyst page
search = requests.post("https://api.notion.com/v1/search", 
    headers=headers, json={"query": "analyst"})

analyst_page = next((p for p in search.json()["results"] 
    if "analyst" in p.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "").lower()), None)

if analyst_page:
    # Create Project Analysis page
    page_data = {
        "parent": {"page_id": analyst_page["id"]},
        "properties": {"title": {"title": [{"text": {"content": "Project Analysis"}}]}},
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "Project Analysis"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Comprehensive analysis of project objectives, progress, and outcomes."}}]}}
        ]
    }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_data)
    print("Created!" if response.status_code == 200 else f"Error: {response.text}")
else:
    print("Analyst page not found")