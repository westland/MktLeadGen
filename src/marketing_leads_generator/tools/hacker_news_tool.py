import os
import requests
from typing import List, Dict, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class HackerNewsSearchInput(BaseModel):
    query: str = Field(..., description="Keywords/product names to search on Hacker News")
    limit: int = Field(default=12, description="Number of results to retrieve")

class HackerNewsSearchTool(BaseTool):
    name: str = "Hacker News Search Tool"
    description: str = "Finds customer reviews, comments, and discussions on Hacker News containing questions or pain points."
    args_schema: Type[BaseModel] = HackerNewsSearchInput

    def _run(self, query: str, limit: int = 12) -> List[Dict]:
        url = "https://hn.algolia.com/api/v1/search"
        params = {
            "query": query,
            "tags": "comment",
            "hitsPerPage": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                print(f"Hacker News API returned status {response.status_code}")
                return []
                
            data = response.json()
            hits = data.get("hits", [])
            results = []
            
            for hit in hits:
                author = hit.get("author", "anonymous")
                comment_text = hit.get("comment_text", "")
                # Algolia Search API returns raw HTML for comments, let's strip HTML tags politely
                from bs4 import BeautifulSoup
                if comment_text:
                    soup = BeautifulSoup(comment_text, "html.parser")
                    text = soup.get_text()
                else:
                    text = ""
                    
                story_id = hit.get("story_id")
                object_id = hit.get("objectID")
                
                url_link = f"https://news.ycombinator.com/item?id={story_id}#id={object_id}" if story_id else "https://news.ycombinator.com"
                
                results.append({
                    "platform": "HackerNews",
                    "url": url_link,
                    "author": author,
                    "title": hit.get("story_title") or "Hacker News Comment",
                    "selftext": text[:1800],
                    "created_at": hit.get("created_at"),
                })
            return results
        except Exception as e:
            print(f"Error querying Hacker News API: {e}")
            return []
