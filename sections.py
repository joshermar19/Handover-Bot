from slack_interface import get_open_channels, get_user_name
from settings import Queries, SectionSettings
from jira_interface import get_tickets
from datetime import date


class LineItem():
    def __init__(self, title, user, created, summary, link):
        self.summary = summary[:SectionSettings.MAX_SUM_LEN]
        self.link = link
        self.base_title = f'*{title} — {user} — {created[:10]}*'

    def jira_line_title(self):
        return self.base_title

    def slack_line_title(self):
        return f'<{self.link}|{self.base_title}>'  # This one includes a Slack formatted hyperlink


class Section():
    def __init__(self, heading, line_items, message_if_none, show_count, no_summaries):
        self.heading = heading
        self.line_items = line_items
        self.message_if_none = message_if_none
        self.show_count = show_count
        self.no_summaries = no_summaries

        print(f'Populated section for "{self.heading}"')

    def get_section(self, for_slack=False):
        title_count = f' ({len(self.line_items)})' if self.show_count else ''
        section_items = [f'*{self.heading}{title_count}:*\n\n']

        if not self.line_items:
            section_items.append(f'_{self.message_if_none}_\n')
        else:
            for li in self.line_items:
                title = li.slack_line_title() if for_slack else li.jira_line_title()
                section_items.append(f'{title}\n')

                # This is useful for channels, as currently they should not have a summary
                if not self.no_summaries:
                    section_items.append(f'{li.summary}\n\n')

        return ''.join(section_items)


class JiraSection(Section):

    def __init__(self, heading, query, message_if_none, show_count=True, no_summaries=False):

        line_items = []

        for issue in get_tickets(query):
            line_items.append(
                LineItem(
                    title=issue.key,
                    user=getattr(issue.fields.assignee, 'name', 'unassigned'),
                    created=issue.fields.created,
                    summary=issue.fields.summary,
                    link=issue.permalink()))

        Section.__init__(
            self,
            heading=heading,
            line_items=line_items,
            message_if_none=message_if_none,
            show_count=show_count,
            no_summaries=no_summaries)


class SlackSection(Section):
    def __init__(self, heading, message_if_none='', show_count=True, no_summaries=True):

        line_items = []

        for channel in get_open_channels():
            line_items.append(
                LineItem(
                    title=channel['name'],
                    user=get_user_name(channel['creator']),
                    created=str(date.fromtimestamp(channel['created'])),
                    summary=channel['topic']['value'],
                    link=f"{SectionSettings.CHN_URL_BASE}{channel['id']}"))

        Section.__init__(
            self,
            heading=heading,
            line_items=line_items,
            message_if_none=message_if_none,
            show_count=show_count,
            no_summaries=no_summaries)


# The following function defines the totality of sections and the order in which they will appear
def get_sections():
    return [
        JiraSection(
            heading='Open Handover Issues',
            query=Queries.HO,
            message_if_none='No open handover issues.',
            show_count=False
        ),
        JiraSection(
            heading='Recent Change Records (-24hrs, any status)',
            query=Queries.CR,
            message_if_none='No recent CR issues.',
            show_count=False
        ),
        JiraSection(
            heading='Recent Outages (-36hrs, any status)',
            query=Queries.P1,
            message_if_none='No recent outages (knock on wood).',
            show_count=False
        ),
        JiraSection(
            heading='Outstanding P2 Incidents',
            query=Queries.P2,
            message_if_none='No outstanding P2 incidents.',
        ),
        JiraSection(
            heading='Outstanding P3 Incidents',
            query=Queries.P3,
            message_if_none='No outstanding P3 incidents.',
        ),
        JiraSection(
            heading='Outstanding P4 Incidents',
            query=Queries.P4,
            message_if_none='No outstanding P4 incidents.',
        ),
        SlackSection(
            heading='Open NOC Channels',
        )]
