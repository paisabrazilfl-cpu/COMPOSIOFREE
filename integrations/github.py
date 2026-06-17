from integrations.base import BaseTool


class GitHubListRepos(BaseTool):
    provider = "github"
    name = "list_repos"

    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        username = parameters.get("username")
        return {
            "success": True,
            "data": {
                "repos": [],
                "username": username,
                "note": "Placeholder implementation",
            },
        }


class GitHubCreateIssue(BaseTool):
    provider = "github"
    name = "create_issue"

    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        repo = parameters.get("repo")
        title = parameters.get("title")
        body = parameters.get("body", "")
        if not all([repo, title]):
            return {"success": False, "error": "Missing required fields: repo, title"}
        return {
            "success": True,
            "data": {
                "repo": repo,
                "title": title,
                "body_preview": str(body)[:120],
                "note": "Placeholder implementation",
            },
        }
