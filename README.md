
# Gmail Support Agent

This is a starter Gmail support agent that integrates directly with your Gmail account using gmail mcp server (community server). The agent can perform various actions including reading emails, drafting emails, sending emails, deleting emails, replying to emails within the same thread, and more. You can use this as starting point and customize this as you like.


---
### 💼 Use Cases Examples: ###

- ✅ Automated Email Triage and Summarization

    - Scenario: Your Gmail inbox quickly becomes cluttered.
    - Usage: The agent can periodically scan your inbox to read incoming emails and generate summaries. It highlights key details (sender, subject, body) to help prioritize important emails.

- 🔁 Smart Email Follow-Up and Reminders

    - Scenario: You often forget to follow up on important emails or tasks.
    - Usage: The agent can identify emails with flags or keywords like "action required" and either send reminders or trigger auto-replies using your templates.

- 📅 Meeting Scheduling and Confirmations

    - Scenario: Coordinating meetings via email is tedious.
    - Usage: The agent can detect meeting requests, parse details (dates/times), and respond with confirmations or proposed slots. Optionally, integrate with Google Calendar for full scheduling support.

- and much more

---




**Repository:**  
[MCP on GitHub](https://github.com/GongRzhe/Gmail-MCP-Server)

---

## Features

- **Read Email:** Retrieve and view your emails.
- **Draft Email:** Create new email drafts.
- **Send Email:** Send out emails.
- **Delete Email:** Remove unwanted emails.
- **Reply to Email:** Reply within the same email thread.
- **Other Features:** Additional functionalities to enhance your Gmail experience.

---



## Prerequisites

Ensure you have the following installed before proceeding:

- **uv:**  
  Make sure `uv` is installed on your system. If not, install it.

- **npx and Node.js:**  
  Ensure you have `npx` installed, which requires Node.js.

---

## Installation

1. **Add the OpenAI Agents Chainlit Package:**
   ```bash
   uv add openai-agents chainlit
   ```

2. **Setup Google Cloud to Enable Gmail Usage:**

   ### a. Create a Google Cloud Project and Enable the Gmail API

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the **Gmail API** for your project.

   ### b. Create OAuth 2.0 Credentials

   - Navigate to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth client ID**.
   - Complete the form (this may involve setting up a consent screen).
   - Choose either **Desktop app** or **Web application** as the application type.
   - Provide a descriptive name and click **Create**.
   - **For Web Applications:** Add `http://localhost:3000/oauth2callback` to the authorized redirect URIs.
   - Download the JSON file containing your OAuth keys.
   - Rename the downloaded file to `gcp-oauth.keys.json`.

3. **Setup test user:**
    ### a. Your account will be created in test mode so you need to add the email in test user so the agent can access the email###
    - Visit [Audience](https://console.cloud.google.com/auth/audience).
    - Scroll down and create test user (Email of the account you want to give the access of).
---


## Authentication

### Global Authentication (Recommended)

1. **Place the OAuth Keys File:**  
   Place the `gcp-oauth.keys.json` file in your home directory where your `pyproject.toml` file is located.

2. Make gmail-mcp directory in the home directory.

3. **Run the Authentication Command:**
   ```bash
   npx @gongrzhe/server-gmail-autoauth-mcp auth
   ```
   This process will:
   - Search for `gcp-oauth.keys.json` in the current directory or in `~/.gmail-mcp/`.
   - If found in the current directory, copy it to `~/.gmail-mcp/`.
   - Open your default browser for Google authentication.
   - Save the obtained credentials as `~/.gmail-mcp/credentials.json`.

---

## Environment Setup

Create a `.env` file in your project directory and add your Gemini API key:
```dotenv
GEMINI_API_KEY="YOUR_API_KEY"
```
> **Note:** Replace `"YOUR_API_KEY"` with your actual Gemini API key.

---

## Running the Agent

To run the Gmail support agent with Chainlit, use the following command:
```bash
uv run chainlit run main.py
```
If you prefer not to have Chainlit open your default browser automatically every time, run it in headless mode and then you can open it on any browser or refresh it if already opened:
```bash
uv run chainlit run main.py --headless
```

---

Enjoy your seamless email management experience with the Gmail Support Agent!