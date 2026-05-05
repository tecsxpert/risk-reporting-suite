# Demo Day Script — Security Reviewer
**Time limit:** 60 Seconds

## What to DO while speaking:
1. Open Postman/Swagger.
2. Hit an endpoint WITHOUT a JWT token -> Point at the 401 error.
3. Hit the Python AI endpoint with <script> -> Point at the 400 error.

## What to SAY (Memorize this):
*"As the Security Reviewer, I implemented a defense-in-depth strategy across our entire stack."*

*   **Bullet 1 (Input):** *"First, I built a Python sanitization middleware that strips HTML tags and actively blocks AI Prompt Injection attempts before they ever reach the Groq API."*
*   **Bullet 2 (Rate Limiting):** *"Second, to protect our free-tier API credits, I configured strict rate limits—30 requests per minute globally, and just 10 on our heavy report generator."*
*   **Bullet 3 (Resilience):** *"Third, I designed the Java-to-Python bridge with strict 10-second timeouts. If the AI service goes down, the main Java app fails gracefully instead of freezing the user."*
*   **Bullet 4 (Hardening):** *"Finally, I ran OWASP ZAP baseline checks and resolved all Medium findings by integrating flask-talisman to enforce strict security headers across all AI responses."*
*   **Close:** *"All findings and mitigations are fully documented in our SECURITY.md."*

## Q&A Backup Answers:
*   **"What happens if a user tries SQL injection?"** 
    -> *"Spring Boot JPA uses parameterized queries by default, making SQLi impossible. For the AI, our regex sanitiser neutralizes it."*
*   **"What happens if the Groq API crashes?"** 
    -> *"Our AiServiceClient catches the timeout and returns a null, allowing the Java app to serve a pre-written fallback template instead of crashing."*
