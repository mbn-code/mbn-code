from github import Github
from datetime import datetime
import pytz
import os

def get_recent_activity(github_token):
    g = Github(github_token)
    user = g.get_user()
    events = user.get_events()
    
    activity_list = []
    count = 0
    
    for event in events:
        if count >= 5:
            break
            
        event_desc = ""
        if event.type == "PullRequestEvent":
            pr = event.payload['pull_request']
            action = event.payload['action']
            event_desc = f"🔀 {action.capitalize()} PR **#{pr['number']}** in **[{event.repo.name}](https://github.com/{event.repo.name})**"
        elif event.type == "CreateEvent":
            repo_name = event.repo.name
            ref_type = event.payload.get('ref_type', '')
            if ref_type == 'repository':
                event_desc = f"📂 Created repository **[{repo_name}](https://github.com/{repo_name})**"
        elif event.type == "PushEvent":
            repo_name = event.repo.name
            commits = event.payload.get('commits', [])
            commit_count = len(commits)
            event_desc = f"📝 Pushed {commit_count} commit(s) to **[{repo_name}](https://github.com/{repo_name})**"
        elif event.type == "IssuesEvent":
            action = event.payload['action']
            issue = event.payload['issue']
            event_desc = f"❗ {action.capitalize()} issue **#{issue['number']}** in **[{event.repo.name}](https://github.com/{event.repo.name})**"
        
        if event_desc:
            activity_list.append(event_desc)
            count += 1
    
    return activity_list

def update_readme():
    utc_now = datetime.now(pytz.UTC)
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create the new activity section
    new_activity = "\n\n## 📈 Recent Activity\n\n"
    new_activity += "**Last Updated:** " + utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + "\n\n"
    
    activities = get_recent_activity(os.getenv('GH_TOKEN'))
    if activities:
        new_activity += "| Recent Activity |\n| --- |\n"
        for activity in activities:
            new_activity += f"| {activity} |\n"
    else:
        new_activity += "*No recent activity*\n"
    
    # Append the new activity section to the end of the README
    updated_content = content.rstrip() + new_activity
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()
