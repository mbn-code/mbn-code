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
        
        if event_desc:
            activity_list.append(event_desc)
            count += 1
    
    return activity_list

def update_readme():
    utc_now = datetime.now(pytz.UTC)
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    marker = "## 🔥 Recent Activity"
    if marker in content:
        parts = content.split(marker)
        new_activity = "\n\n**Last Updated:** " + utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + "\n\n| Activity |\n| --- |\n"
        activities = get_recent_activity(os.getenv('GH_TOKEN'))
        for activity in activities:
            new_activity += f"| {activity} |\n"
        updated_content = parts[0] + marker + new_activity + parts[1]
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(updated_content)

if __name__ == "__main__":
    update_readme()
