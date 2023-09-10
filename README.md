# Argos
Argos watches web pages for changes and sends Telegram notifications when they are detected.

Use the targets.py.sample file to create your targets.py file.

Create a secrets.py file with the following content:

```
CHAT_IDS = [your-chat-id, any-other-chat-ids]
TOKEN = 'telegram-bot-token:secret'
```

Then build and run the Docker container with the build.sh script.
