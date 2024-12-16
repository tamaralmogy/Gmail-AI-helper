import pyautogui
import time
import pyperclip


def send_fetch_prompt_to_claude(num_emails: int):
    """
    Use PyAutoGUI to send a general fetch prompt to Claude Desktop.
    Args:
        num_emails (int): Number of emails to fetch.
    """
    # Construct the general fetch prompt
    fetch_prompt = (
        f"Retrieve the first {num_emails} emails from my Gmail account. "
        f"For each email, provide the subject and sender in JSON format: Subject: ..."
        "Sender: .... "
        "]"
    )

    # Focus the Claude Desktop window
    print("Switch to the Claude Desktop window now!")
    time.sleep(5)

    # Type the fetch prompt
    pyautogui.typewrite(fetch_prompt, interval=0.05)
    pyautogui.press("enter")
    print("Fetch prompt sent to Claude!")

    # Wait for Claude to fetch emails
    time.sleep(15)

def copy_claude_response():
    """
    Copy Claude's response from the desktop.
    """
    print("Copying Claude's response...")
    pyautogui.hotkey("ctrl", "a")  # Select all text
    pyautogui.hotkey("ctrl", "c")  # Copy selected text

    # Retrieve text from the clipboard
    response_text = pyperclip.paste()
    print("Response copied from Claude.")
    return response_text

def send_categorization_prompt_to_claude(emails_response: str):
    """
    Send a categorization prompt to Claude Desktop using the copied email response.
    Args:
        emails_response (str): The JSON or text response copied from Claude.
    """
    # Construct the categorization prompt
    prompt = (
        "Please categorize each of these emails into one of the following categories: "
        "(Work, School, Shopping, Family, Friends, Other). "
        "Also, rank the email by priority (Urgent,Not Urgent) and (Important, Not Important). "
        "Response example: The following email is categorized as School and is Important but not Urgent...:\n\n"
        f"{emails_response}"  # Paste the copied email response here
    )

    # Type the categorization prompt
    pyautogui.typewrite(prompt, interval=0.05)
    pyautogui.press("enter")
    print("Categorization prompt sent to Claude!")

    # Wait for Claude to categorize
    time.sleep(15)

def stop_claude():
    """
    Send a final command to Claude to stop generating responses.
    """
    print("Sending stop command to Claude...")
    pyautogui.typewrite("Thank you. Stop.", interval=0.05)
    pyautogui.press("enter")
    print("Stop command sent.")


def main():
    num_emails = 5  # Number of emails to fetch

    # Step 1: Send fetch prompt to Claude
    send_fetch_prompt_to_claude(num_emails)

    # Step 2: Copy Claude's response
    emails_response = copy_claude_response()

    # Step 3: Send categorization prompt with the copied response
    send_categorization_prompt_to_claude(emails_response)

    # Step 4: Stop Claude from continuing
    stop_claude()
    
    print("Process completed! Check the categorization response in Claude Desktop.")

if __name__ == "__main__":
    main()