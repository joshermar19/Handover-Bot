from settings import Queries, SectionSettings
from datetime import date
import slack_interface
import jira_interface
import followup


class LineItem():
    def __init__(self, **fields):
        self.fields = fields

    # These methods return the base with any vars expanded from the item itself
    def jira_line_title(self, base):
        return base.format(**self.fields)

    def slack_line_title(self, base):
        return f'<{self.fields["link"]}|{base.format(**self.fields)}>'
        # f'<{self.fields['link']}|{self.base_title}>'  # This one includes a Slack formatted hyperlink


class Section():
    def __init__(self, heading, line_items, base, message_if_none, show_count):
        self.heading = heading
        self.line_items = line_items
        self.base = base
        self.message_if_none = message_if_none
        self.show_count = show_count

        print(f'Populated section for "{self.heading}"')

    def get_section(self, for_slack=False):
        title_count = f' ({len(self.line_items)})' if self.show_count else ''

        section_items = []

        if self.heading:
            section_items.append(f'*{self.heading}{title_count}:*\n\n')

        if not self.line_items:
            section_items.append(f'_{self.message_if_none}_\n')
        else:
            for li in self.line_items:
                title = li.slack_line_title(self.base) if for_slack else li.jira_line_title(self.base)
                section_items.append(f'{title}\n{li.fields["summary"]}\n')

        return ''.join(section_items)


class SecFromJira(Section):
    def __init__(self, heading, issues, base, message_if_none='', show_count=True):

        line_items = []

        for issue in issues:
            line_items.append(
                LineItem(
                    key=issue.key,
                    priority=issue.fields.priority.name,
                    created=issue.fields.created[:10],
                    updated=issue.fields.updated[:16].replace('T', '_'),
                    summary=issue.fields.summary[:80],  # Sadly, I don't know where else to limit the len
                    link=issue.permalink()))

        Section.__init__(
            self,
            heading=heading,
            line_items=line_items,
            base=base,
            message_if_none=message_if_none,
            show_count=show_count)


class SecFromSlack(Section):
    def __init__(self, heading, base, message_if_none='', show_count=True):

        line_items = []

        for channel in slack_interface.get_open_channels():
            line_items.append(
                LineItem(
                    key=channel['name'],
                    # user=slack_interface.get_user_name(channel['creator']),
                    created=str(date.fromtimestamp(channel['created'])),
                    summary=channel['topic']['value'][:70],
                    link=f"{SectionSettings.CHN_URL_BASE}{channel['id']}"))

        Section.__init__(
            self,
            heading=heading,
            line_items=line_items,
            base=base,
            message_if_none=message_if_none,
            show_count=show_count)


# The following function defines the totality of sections and the order in which they will appear
def get_sections():
    return [
        SecFromJira(
            heading='Open Handover Issues',
            issues=jira_interface.get_tickets(Queries.HO),
            message_if_none='No open handover issues.',
            base=SectionSettings.SHORT_BASE,
            show_count=False
        ),
        SecFromJira(
            heading='Recent Change Records (-24hrs, any status)',
            issues=jira_interface.get_tickets(Queries.CR),
            message_if_none='No recent CR issues.',
            base=SectionSettings.SHORT_BASE,
            show_count=False
        ),
        SecFromJira(
            heading='Recent Outages (-36hrs, any status)',
            issues=jira_interface.get_tickets(Queries.P1),
            message_if_none='No recent outages (knock on wood).',
            base=SectionSettings.LONG_BASE,
            show_count=False
        ),
        SecFromJira(
            heading='Outstanding Incidents',
            issues=jira_interface.get_tickets(Queries.OPEN_ISSUES),
            message_if_none='No outstanding incidents. Woohoo!',
            base=SectionSettings.LONG_BASE,
        ),
        SecFromSlack(
            heading='Open NOC Channels',
            base=SectionSettings.SHORT_BASE,
        )]


def get_followup_section():
    followup_issues = followup.get_followup_issues()

    if not followup_issues:
        return None

    return SecFromJira(
        heading='',
        issues=followup_issues,
        base=SectionSettings.LONG_BASE,
        show_count=False)
