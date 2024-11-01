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
            event_desc = f"💻 Pushed code to [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "CreateEvent":
            repo_name = event.repo.name
            event_desc = f"🎉 Created repository [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "IssuesEvent":
            issue = event.payload['issue']
            event_desc = f"📝 {event.payload['action'].capitalize()} issue #{issue['number']} in [{event.repo.name}]({issue['html_url']})"
        elif event.type == "PullRequestEvent":
            pr = event.payload['pull_request']
            event_desc = f"🔃 {event.payload['action'].capitalize()} PR #{pr['number']} in [{event.repo.name}]({pr['html_url']})"
        elif event.type == "ForkEvent":
            repo_name = event.repo.name
            event_desc = f"🍴 Forked [{repo_name}](https://github.com/{repo_name})"
        elif event.type == "WatchEvent":
            repo_name = event.repo.name
            event_desc = f"⭐ Starred [{repo_name}](https://github.com/{repo_name})"
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
    activity_section = "\n<details>\n"
    activity_section += "<summary><b>🔥 Recent GitHub Activity</b></summary>\n\n"
    
    # Add timestamp with emoji
    utc_now = datetime.now(pytz.UTC)
    activity_section += f"<div align='center'>\n\n"
    activity_section += f"🕐 Last Updated: `{utc_now.strftime('%Y-%m-%d %H:%M')} UTC`\n\n"
    activity_section += "</div>\n\n"
    
    # Add activities with better formatting
    activity_section += "<table>\n<tr><td width='100%'>\n\n"
    for activity in activities:
        activity_section += f"▪️ {activity}\n"
    activity_section += "\n</td></tr>\n</table>\n\n"
    activity_section += "</details>\n"
    
    # Check if recent activity section already exists
    if "<summary><b>🔥 Recent GitHub Activity</b></summary>" in content:
        # Replace existing section
        parts = content.split("<details>")
        content = parts[0] + activity_section
        if len(parts) > 2:
            content += "<details>" + "".join(parts[2:])
    else:
        # Add new section at the end
        content = content.strip() + "\n\n" + activity_section
    
    # Write updated content back to README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
