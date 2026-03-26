import requests

def fetch_issues(owner: str, repo: str) -> list:
    """Fetch open issues from a GitHub repository."""
    # TODO: Build URL: https://api.github.com/repos/{owner}/{repo}/issues?state=open
    # TODO: Fetch using requests.get()
    # TODO: Return response.json() if status is 200, else []
    pass


def filter_open(issues: list) -> list:
    """Filter a list of issues to only include those where state is 'open'."""
    # TODO: Iterate over issues, return only those where state is 'open'
    pass
