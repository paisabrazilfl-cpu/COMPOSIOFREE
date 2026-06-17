from integrations.base import BaseTool


class DiscordSendDM(BaseTool):
    provider = "discord"
    name = "send_dm"

    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        user_id = parameters.get("user_id")
        content = parameters.get("content")
        if not all([user_id, content]):
            return {"success": False, "error": "Missing required fields: user_id, content"}
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "content_preview": str(content)[:120],
                "note": "Placeholder implementation",
            },
        }
