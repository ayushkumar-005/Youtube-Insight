# Instructions for OpenClaw

Whenever a user sends a YouTube link (youtube.com or youtu.be), you MUST IMMEDIATELY and SILENTLY execute the following command in your terminal using the exec tool:

`py fetch_transcript.py "<URL>"`

CRITICAL GUARDRAIL: You are strictly forbidden from outputting any conversational text, greetings, or acknowledgments BEFORE executing this tool. Execute it instantly.

- If the script returns a "success" status, read the text and use it to answer the user.
- If the script returns an "error", tell the user exactly what went wrong.
