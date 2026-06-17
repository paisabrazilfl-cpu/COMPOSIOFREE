from integrations.base import BaseTool
from integrations.gmail import GmailSendEmail, GmailListEmails
from integrations.github import GitHubListRepos, GitHubCreateIssue
from integrations.slack import SlackPostMessage
from integrations.discord import DiscordSendDM
from integrations.google_calendar import GoogleCalendarListEvents
from integrations.google_sheets import GoogleSheetsReadSheet


REGISTRY = {
    "gmail.send_email": GmailSendEmail,
    "gmail.list_emails": GmailListEmails,
    "github.list_repos": GitHubListRepos,
    "github.create_issue": GitHubCreateIssue,
    "slack.post_message": SlackPostMessage,
    "discord.send_dm": DiscordSendDM,
    "google_calendar.list_events": GoogleCalendarListEvents,
    "google_sheets.read_sheet": GoogleSheetsReadSheet,
}


def get_tool(tool_key: str) -> BaseTool:
    cls = REGISTRY.get(tool_key)
    if not cls:
        raise KeyError(f"Unknown tool: {tool_key}")
    return cls()
