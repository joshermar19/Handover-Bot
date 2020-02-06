from settings import TZ, Queries, Intervals
from datetime import datetime
import jira_interface


def _needs_followup(issue, p, t):
        '''Following a pretty straightforward lexical convention, this funciton should simply return True/False'''

        last_touched = datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z')

        # Simple concept calls for parsimony of var naming I think
        _d = t - last_touched
        time_since = _d.total_seconds()  # SECONDS since ticket was last touched

        should_followup = (  # Will either be True or False
            p == 2 and time_since > Intervals.P2 or
            p == 3 and time_since > Intervals.P3 or
            p == 4 and time_since > Intervals.P4
        )

        return should_followup


def get_followup_issues():
    all_outstanding = jira_interface.get_tickets(Queries.OPEN_ISSUES)
    now = datetime.now(TZ)

    followup_issues = []
    for issue in all_outstanding:
        priority = int(issue.fields.priority.id)

        if _needs_followup(issue, priority, now):
            followup_issues.append(issue)

    return followup_issues
