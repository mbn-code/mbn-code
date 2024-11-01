from github import Github
from datetime import datetime
import pytz
import os

def get_recent_activity(github_token, max_events=5):
    g = Github(github_token)
    user = g.get_user()
    events = user.get_events()
    
    activity_list = []
    count = 0
    
    for event in events:
        if count >= max_events:
            break
            
        event_desc = ""
        if event.type == "PushEvent":
            repo_name = event.repo.name
            event_desc = f"🔨 Pushed to **[{repo_name}](https://github.com/{repo_name})**"
        elif event.type == "CreateEvent":
            repo_name = event.repo.name
            event_desc = f"📂 Created repository **[{repo_name}](https://github.com/{repo_name})**"
        elif event.type == "IssuesEvent":
            issue = event.payload.get('issue', {})
            action = event.payload.get('action', '').capitalize()
            event_desc = f"❗ {action} issue **#{issue.get('number')}** in **[{event.repo.name}](https://github.com/{event.repo.name})**"
        elif event.type == "PullRequestEvent":
            pr = event.payload.get('pull_request', {})
            action = event.payload.get('action', '').capitalize()
            event_desc = f"🔀 {action} PR **#{pr.get('number')}** in **[{event.repo.name}](https://github.com/{event.repo.name})**"
        elif event.type == "ForkEvent":
            forkee = event.payload.get('forkee', {})
            event_desc = f"🍴 Forked **[{forkee.get('full_name')}](https://github.com/{forkee.get('full_name')})**"
        
        if event_desc:
            activity_list.append(event_desc)
            count += 1
    
    return activity_list

def update_readme():
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print(f"{readme_path} does not exist.")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    github_token = os.getenv('GH_TOKEN')
    if not github_token:
        print("GH_TOKEN environment variable not set.")
        return
    
    activities = get_recent_activity(github_token)
    
    utc_now = datetime.now(pytz.UTC)
    activity_section = "\n## 🔥 Recent Activity\n\n"
    activity_section += f"**Last Updated:** {utc_now.strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
    activity_section += "| Activity |\n| --- |\n"
    for activity in activities:
        activity_section += f"| {activity} |\n"
    
    if "## 🔥 Recent Activity" in content:
        content = content.split("## 🔥 Recent Activity")[0] + activity_section
    else:
        content = content.strip() + "\n\n" + activity_section
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()