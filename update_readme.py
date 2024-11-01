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
        if count >= 5:  # Get last 5 activities
            break
            
        event_desc = ""
        if event.type == "PushEvent":
            repo_name = event.repo.name
            event_desc = f"🔨 Pushed to [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "CreateEvent":
            repo_name = event.repo.name
            event_desc = f"📂 Created repository [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "IssuesEvent":
            issue = event.payload['issue']
            event_desc = f"❗ {event.payload['action'].capitalize()} issue #{issue['number']} in [{event.repo.name}]({issue['html_url']})"
        elif event.type == "PullRequestEvent":
            pr = event.payload['pull_request']
            event_desc = f"🔀 {event.payload['action'].capitalize()} PR #{pr['number']} in [{event.repo.name}]({pr['html_url']})"
        
        if event_desc:
            activity_list.append(event_desc)
            count += 1
    
    return activity_list

def update_readme():
    # Read existing README content
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get recent activity
    github_token = os.getenv('GH_TOKEN')
    activities = get_recent_activity(github_token)
    
    # Create recent activity section
    utc_now = datetime.now(pytz.UTC)
    activity_section = "\n## 🔥 Recent Activity\n\n"
    activity_section += f"Last Updated: {utc_now.strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
    for activity in activities:
        activity_section += f"• {activity}\n"
    
    # Check if recent activity section already exists
    if "## 🔥 Recent Activity" in content:
        # Replace existing section
        content = content.split("## 🔥 Recent Activity")[0] + activity_section
    else:
        # Add new section at the end
        content = content.strip() + "\n\n" + activity_section
    
    # Write updated content back to README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()