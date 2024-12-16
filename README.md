# Mail AI Helper

The **Mail AI Helper** is a Python-based application that integrates with Claude Desktop and the Gmail API to fetch, process, and categorize emails intelligently. By leveraging AI for email organization, this tool automates tedious tasks, such as retrieving email metadata, categorizing emails, and prioritizing them.

---

## **Features**

1. **Fetch Emails**:

   - Retrieves emails from Gmail using the Gmail API.
   - Extracts metadata such as the subject and sender.

2. **Categorize Emails**:

   - Sends fetched emails to Claude Desktop for categorization.
   - Categories include `Work`, `School`, `Shopping`, `Family`, `Friends`, and `Other`.

3. **Rank Email Priority**:

   - Claude assigns priorities such as `Urgent\Not Urgent`, `Important\Not Important` to each email.

4. **Interactive Workflow**:

   - Uses PyAutoGUI to interact with Claude Desktop seamlessly.
   - Automates typing and copying tasks for Claude Desktop interactions.

5. **MCP Integration**:

   - The tool integrates with MCP (Model Context Protocol) for Claude Desktop.
   - Implements the custom `get-emails` tool to fetch emails from the user’s logged-in Gmail account.

---

## **Setup and Installation**

### Prerequisites

- Python 3.10 or later
- Gmail API enabled on your Google Cloud account
- Claude Desktop installed

### Installation Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mail-ai-helper
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv/Scripts/activate
   ```

3. Install dependencies:

   ```bash
   uv add .
   ```

4. Add the `.gitignore` file:
   Ensure sensitive files and directories like `.venv/`, `credentials.json`, and `token.json` are excluded.

   Example `.gitignore`:

   ```plaintext
   .venv/
   credentials.json
   token.json
   ```

5. Set up the Gmail API:

   - Create a `credentials.json` file by enabling the Gmail API in your Google Cloud account.
   - Place `credentials.json` in the root directory.

6. Authenticate Gmail:
   Run the authentication script to generate a `token.json` file:

   ```bash
   uv run src/mail/auth.py
   ```

---

## **Usage**

### Running the Mail AI Helper

1. Fetch emails and categorize them:

   ```bash
   uv run src/mail/fetch_emails.py
   ```

2. Follow the instructions:

   - Switch to Claude Desktop when prompted.
   - Let the script interact with Claude to fetch and categorize emails.
   - Review and verify results in Claude Desktop.

### Workflow Example

1. The script sends a prompt to Claude asking it to retrieve emails.
2. Claude outputs the email metadata in JSON format.
3. The script copies the response and sends a new prompt to categorize and prioritize the emails.
4. Claude provides categorized and prioritized results, which can be reviewed directly.

---

## **Project Structure**

```
mail-ai-helper/
├── auth.py                  # Handles Gmail API authentication
├── fetch_emails.py          # Main script for fetching and categorizing emails
├── requirements.txt         # Python dependencies
├── .gitignore               # Excluded files and directories
└── README.md                # Project documentation
```

---

## **Technical Details**

### Fetching Emails

- Uses the Gmail API to retrieve email metadata (e.g., subject, sender).
- Interacts with Claude Desktop using PyAutoGUI for automated prompts.
- Utilizes the MCP `get-emails` tool for email fetching.

### Categorization and Prioritization

- Sends a follow-up prompt for Categorization and Prioritization.

---

## **Example Output**

### Fetched Emails:

```json
[
  { "subject": "Meeting Reminder", "sender": "boss@example.com" },
  { "subject": "Shopping Deals", "sender": "promo@shopping.com" },
  { "subject": "Class Schedule Update", "sender": "professor@school.com" }
]
```

### Categorized Emails:

```json
[
  {
    "subject": "Meeting Reminder",
    "sender": "boss@example.com",
    "category": "Work",
    "priority": "Important"
  },
  {
    "subject": "Shopping Deals",
    "sender": "promo@shopping.com",
    "category": "Shopping",
    "priority": "Low"
  },
  {
    "subject": "Class Schedule Update",
    "sender": "professor@school.com",
    "category": "School",
    "priority": "Urgent"
  }
]
```

---

## **Security Note**

### Handle Sensitive Data Wisely

This application interacts with sensitive data such as email credentials and content. Follow these best practices to ensure security:

- **Never Share Credentials**: Keep `credentials.json` and `token.json` private and secure.
- **Use .gitignore**: Ensure sensitive files are excluded from version control.
- **Rotate Credentials Regularly**: Change API keys and tokens periodically.
- **Advice Official Documentation**: Refer to the official [Model Context Protocol Documentation](https://modelcontextprotocol.io/introduction) for additional security and best practices.

---

## **Future Improvements**

- Automate JSON saving and response parsing.
- Add OCR for capturing responses from Claude Desktop.
- Expand categorization with custom labels and priorities.
- Add support for email attachments and advanced filtering.

---
