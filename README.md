# Slack bot summarize
## 1. Install and setup environtment 
### 1.1 Prepare key for Gemini
#### Create key for Gemini
- Access link https://aistudio.google.com/apikey, create your account and choose Create API Key.
- Reference link: https://www.youtube.com/watch?v=o8iyrtQyrZM.
### 1.2 Create your workspace in Slack and add roles for Bot
#### Create Slack Bot 
- Access link https://slack.com/, create your workspace.
- Access link https://api.slack.com/, create your account and choose Your apps -> Create New App -> From Scratch.
- Follow the video https://www.youtube.com/watch?v=KJ5bFv-IRFM&list=PLzMcBGfZo4-kqyzTzJWCV6lyK-ZMYECDc from the beginning to 5:25.
#### Add roles for Bot
- Choose OAuth & Permissionsin Features of your bot.
- Add roles app_mentions:read, assistant:write, calls:read, calls:write, canvases:read, canvases:write, channels:history, channels:manage, channels:read, chat:write, chat:write.customize, chat:write.public, files:write, groups:history, groups:write, im:history, im:read, im:write, links.embed:write, links:read, links:write, mpim:history, mpim:write, remote_files:read, remote_files:share, remote_files:write, usergroups:read, usergroups:write, users:read, users:write in Bot Token Scopes.     
### 1.3 Prepare for running 
### Clone repository
```bash git clone https://github.com/username/repo-name.git```
#### Create file .env in slack_bot_sum\slack_assistant\assistant
## 2. Running Bot
