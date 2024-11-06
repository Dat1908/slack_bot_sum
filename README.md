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
- Copy Bot User OAuth Token: xoxb-...
#### Add roles for Bot
- Choose OAuth & Permissionsin Features of your bot.
- Add roles app_mentions:read, assistant:write, calls:read, calls:write, canvases:read, canvases:write, channels:history, channels:manage, channels:read, chat:write, chat:write.customize, chat:write.public, files:write, groups:history, groups:write, im:history, im:read, im:write, links.embed:write, links:read, links:write, mpim:history, mpim:write, remote_files:read, remote_files:share, remote_files:write, usergroups:read, usergroups:write, users:read, users:write in Bot Token Scopes.     
### 1.3 Prepare for running 
#### Clone repository
```git clone https://github.com/Dat1908/slack_bot_sum.git```
#### Create file .env in slack_bot_sum\slack_assistant\assistant
- This file include: MODEL_NAME = gemini-1.5-flash, GOOGLE_API_KEY = [your key], SLACK_BOT_TOKEN = [your key]
#### Set up environtment
- ```pip install -r requirements.txt```
## 2. Running Bot
- Run file app.py
