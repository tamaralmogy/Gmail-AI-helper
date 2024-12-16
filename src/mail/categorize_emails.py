import asyncio
import pyautogui
import time
from mail.auth import get_gmail_service
from mail.server import query_gmail, format_email

def send_to_claude_via_pyautogui(email_content: str):
    """
    Use PyAutoGUI to send a prompt to Claude Desktop.
    Args:
        email_content (str): Formatted email content with subject and sender.
    """
    # Construct the prompt for Claude
    prompt = (
        f"The following email was received:\n"
        f"{email_content}\n\n"
        "Please categorize this email into one of the following categories: "
        "(Work, School, Shopping, Family, Friends, Other). "
        "Also, rank the email by priority (Urgent, Important, Normal, Low)."
        "Response example: The following email is categorized as [x] and has priority [y]"
    )

    # Focus the Claude Desktop window
    print("Switch to the Claude Desktop window now!")
    time.sleep(5)  # Allow time to manually switch to the window

    # Type the prompt
    pyautogui.typewrite(prompt, interval=0.05)  # Type each character with a slight delay

    # Press Enter to send the prompt
    pyautogui.press("enter")
    print("Prompt sent to Claude!")

    # Wait for Claude to process the input
    time.sleep(10)  # Adjust this based on response time

    print("Check the Claude response manually or capture it programmatically.")

async def categorize_emails():
    # Step 1: Fetch emails
    max_results = 5  # Number of emails to fetch
    service = get_gmail_service()
    emails = await query_gmail(service, max_results)

    if not emails:
        print("No emails found.")
        return

    # Step 2: Process each email
    for email_metadata in emails:
        # Reuse format_email function to extract subject and sender
        email_content = format_email(service, email_metadata)

        # Send prompt to Claude Desktop
        send_to_claude_via_pyautogui(email_content)

        # Wait for manual verification of the response before continuing
        input("Press Enter after processing this email...")

    print("Email categorization completed!")


# Main entry point
if __name__ == "__main__":
    asyncio.run(categorize_emails())