import requests

headers = {
    "Authorization": "Bearer ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Find Analista page
search = requests.post("https://api.notion.com/v1/search", headers=headers, json={"query": "Analista"}, verify=False)
analyst = next((p for p in search.json()["results"] if "analista" in str(p).lower()), None)

if analyst:
    # Create Project Analysis blog
    blog = {
        "parent": {"page_id": analyst["id"]},
        "properties": {"title": {"title": [{"text": {"content": "Project Analysis"}}]}},
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "Project Analysis"}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Executive Summary"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "This comprehensive analysis evaluates project performance, key metrics, and strategic outcomes."}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Key Findings"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Project objectives alignment with business goals"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Resource utilization and efficiency metrics"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Risk assessment and mitigation strategies"}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Recommendations"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Based on the analysis, we recommend continued monitoring of key performance indicators and implementation of suggested improvements."}}]}}
        ]
    }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=blog, verify=False)
    print("Blog created successfully!" if response.status_code == 200 else f"Error: {response.text}")
else:
    print("Analista page not found")