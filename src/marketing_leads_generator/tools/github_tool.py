import os
import requests
from typing import List, Dict, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class GitHubSearchInput(BaseModel):
    query: str = Field(..., description="GitHub search query (e.g. 'alternative to' or 'bug' keywords)")
    limit: int = Field(default=12, description="Number of issues/comments to retrieve")

class GitHubSearchTool(BaseTool):
    name: str = "GitHub Discussions & Issues Search Tool"
    description: str = "Searches issues and discussions on GitHub containing user questions, requests for recommendations, or pain points."
    args_schema: Type[BaseModel] = GitHubSearchInput

    def _run(self, query: str, limit: int = 12) -> List[Dict]:
        token = os.getenv("GITHUB_TOKEN")
        
        # GitHub Search API endpoint for issues/PRs
        url = "https://api.github.com/search/issues"
        
        headers = {
            "Accept": "application/vnd.github+json"
        }
        if token:
            headers["Authorization"] = f"token {token}"
            
        params = {
            "q": query,
            "per_page": limit,
            "sort": "updated",
            "order": "desc"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                print(f"GitHub Search API returned status {response.status_code}")
                # Return empty list or fallback error message
                return []
                
            data = response.json()
            items = data.get("items", [])
            results = []
            
            for item in items:
                author_info = item.get("user", {})
                author = author_info.get("login", "anonymous")
                body = item.get("body") or ""
                
                results.append({
                    "platform": "GitHub",
                    "url": item.get("html_url"),
                    "author": author,
                    "title": item.get("title") or "GitHub Issue/Discussion",
                    "selftext": body[:1800],
                    "created_at": item.get("created_at"),
                })
            return results
        except Exception as e:
            print(f"Error querying GitHub Search API: {e}")
            return []
