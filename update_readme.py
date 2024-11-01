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
            commits = event.payload.get('commits', [])
            if commits:
                message = commits[0].get('message', '').split('\n')[0][:60]
                event_desc = f"🚀 Pushed: \"{message}\" to [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "CreateEvent":
            repo_name = event.repo.name
            ref_type = event.payload.get('ref_type', '')
            if ref_type == 'repository':
                event_desc = f"📂 Created new repository [{repo_name}](https://github.com/{repo_name})"
            elif ref_type:
                event_desc = f"🌿 Created {ref_type} in [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "IssuesEvent":
            issue = event.payload['issue']
            event_desc = f"📝 {event.payload['action'].capitalize()} issue \"#{issue['number']}: {issue['title']}\" in [{event.repo.name}]({issue['html_url']})"
        elif event.type == "PullRequestEvent":
            pr = event.payload['pull_request']
            event_desc = f"🔄 {event.payload['action'].capitalize()} PR \"#{pr['number']}: {pr['title']}\" in [{event.repo.name}]({pr['html_url']})"
        elif event.type == "ReleaseEvent":
            release = event.payload['release']
            event_desc = f"📦 {event.payload['action'].capitalize()} release \"{release['name']}\" in [{event.repo.name}]({release['html_url']})"
        elif event.type == "PublicEvent":
            repo_name = event.repo.name
            event_desc = f"🌟 Made [{repo_name}](https://github.com/{repo_name}) public"
        
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
    
    # Create recent activity section with enhanced styling
    utc_now = datetime.now(pytz.UTC)
    
    activity_section = "\n## 🎯 My Recent Activity\n\n"
    activity_section += f"<div align='center'>\n\n"
    activity_section += f"*Last Updated: `{utc_now.strftime('%Y-%m-%d %H:%M')} UTC`*\n\n"
    activity_section += "</div>\n\n"
    
    # Add activities with better formatting
    for activity in activities:
        activity_section += f"- {activity}\n"
    
    # Replace existing section or add new one
    if "## 🎯 My Recent Activity" in content:
        parts = content.split("## 🎯 My Recent Activity")
        new_content = parts[0].rstrip() + activity_section
        if len(parts) > 1:
            remaining = parts[1].split("\n##", 1)
            if len(remaining) > 1:
                new_content += "\n##" + remaining[1]
        content = new_content
    else:
        content = content.rstrip() + "\n\n" + activity_section
    
    # Write updated content back to README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
