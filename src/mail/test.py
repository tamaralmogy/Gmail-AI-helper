import asyncio
from mail.auth import get_gmail_service
from mail.server import query_gmail, format_email


async def test_gmail():
    """
    Test the Gmail service to fetch and format emails.
    """
    # Step 1: Authenticate and get Gmail service
    service = get_gmail_service()

    # Step 2: Fetch the first 5 emails
    max_results = 5
    print(f"Fetching the first {max_results} emails...")
    emails = await query_gmail(service, max_results)

    if emails:
        print("\nFetched emails:")
        for email_metadata in emails:
            formatted_email = format_email(service, email_metadata)
            print(formatted_email)
    else:
        print("No emails found or failed to fetch.")

if __name__ == "__main__":
    asyncio.run(test_gmail())
