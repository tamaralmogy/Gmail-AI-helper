import pyautogui
import time
import pyperclip


def send_combined_prompt_to_claude(num_emails: int):
    """
    Use PyAutoGUI to send a combined fetch and categorization prompt to Claude Desktop.
    Args:
        num_emails (int): Number of emails to fetch and categorize.
    """
    # Construct the combined fetch and categorization prompt
    combined_prompt = (
        f"Retrieve the first {num_emails} emails from my Gmail account. "
        f"For each email, provide the subject and sender in JSON format. Then, categorize each email into one of the following categories: "
        f"(Work, School, Shopping, Family, Friends, Other). Additionally, rank each email by priority: "
        f"(Urgent, Not Urgent) and (Important, Not Important). "
        f"Response example: {{'Subject': '...', 'Sender': '...', 'Category': 'School', 'Priority': 'Urgent, Important'}}"
    )

    # Focus the Claude Desktop window
    print("Switch to the Claude Desktop window now!")
    time.sleep(5)

    # Type the combined prompt
    pyautogui.typewrite(combined_prompt, interval=0.05)
    pyautogui.press("enter")
    print("Combined prompt sent to Claude!")

    # Wait for Claude to process the request
    time.sleep(20)


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


def stop_claude():
    """
    Send a final command to Claude to stop generating responses.
    """
    print("Sending stop command to Claude...")
    pyautogui.typewrite("Thank you. Stop.", interval=0.05)
    pyautogui.press("enter")
    print("Stop command sent.")


def main():
    num_emails = 10 # Number of emails to fetch and categorize

    # Step 1: Send combined fetch and categorization prompt to Claude
    send_combined_prompt_to_claude(num_emails)

    # Step 2: Copy Claude's response
    categorized_response = copy_claude_response()

    # Step 3: Stop Claude from continuing
    stop_claude()

    # Step 4: Print the final categorized response
    print("Process completed! Check the categorization response below:")
    print(categorized_response)


if __name__ == "__main__":
    main()
