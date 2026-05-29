import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

slack_app = App(token=os.getenv("SLACK_BOT_TOKEN"))

def send_reminder(slack_user_id: str, owner: str,
                  deliverable: str, recipient: str, deadline):
    try:
        slack_app.client.chat_postMessage(
            channel=slack_user_id,
            text=(
                f"Hi {owner} 👋 — you have an open commitment:\n\n"
                f"*What:* {deliverable}\n"
                f"*To:* {recipient}\n"
                f"*Due:* {deadline.strftime('%B %d, %Y')}\n\n"
                f"Reply `done` to mark it complete or visit "
                f"{os.getenv('APP_URL')}/dashboard to update."
            )
        )
        return True
    except Exception as e:
        print(f"Slack reminder failed: {e}")
        return False

@slack_app.message("done")
def handle_done(message, say):
    say("Got it — head to your dashboard to mark it complete.")

def start_socket_mode():
    handler = SocketModeHandler(
        slack_app,
        os.getenv("SLACK_APP_TOKEN")
    )
    handler.start()