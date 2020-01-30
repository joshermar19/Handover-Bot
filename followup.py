from datetime import datetime
from jira_interface import get_tickets
from settings import TZ, Queries, Intervals


def _needs_followup(issue, p, t):
        '''Following a pretty straightforward lexical convention, this funciton should simply return True/False'''

        last_touched = datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z')

        # Simple concept calls for parsimony of var naming I think
        _d = t - last_touched
        d_secs = _d.total_seconds()

        # DEBUG
        print(issue)
        print(last_touched)
        print(f'Was {d_secs/3600} hrs ago')
        print('-----------------')

        should_followup = (
            p == 2 and d_secs > Intervals.P2 or
            p == 3 and d_secs > Intervals.P3 or
            p >= 4 and d_secs > Intervals.P4P5
        )

        return should_followup  # True/False


def get_followup_issues():
    all_outstanding = get_tickets(Queries.ALL)
    now = datetime.now(TZ)

    followup_issues = []

    for issue in all_outstanding:
        priority = int(issue.fields.priority.id)

        if _needs_followup(issue, priority, now):
            followup_issues.append(issue)

    return followup_issues
