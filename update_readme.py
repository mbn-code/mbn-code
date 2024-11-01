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
            event_desc = f"🔀 {action.capitalize()} PR #{pr['number']} in {event.repo.name}"
        elif event.type == "CreateEvent":
            repo_name = event.repo.name
            ref_type = event.payload.get('ref_type', '')
            if ref_type == 'repository':
                event_desc = f"📂 Created repository {repo_name}"
        
        if event_desc:
            activity_list.append(event_desc)
            count += 1
    
    return activity_list

def update_readme():
    utc_now = datetime.now(pytz.UTC)
    
    activity_section = "\n\nLast Updated: " + utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + "\n\n"
    activity_section += "Activity\n"
    
    activities = get_recent_activity(os.getenv('GH_TOKEN'))
    
    for activity in activities:
        activity_section += f"{activity}\n"
    
    with open('README.md', 'a', encoding='utf-8') as f:
        f.write(activity_section)

if __name__ == "__main__":
    update_readme()
