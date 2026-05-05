PRIMARY_PROMPT = """
You are a professional risk analyst.
Rewrite the input into a single formal statement using exactly this format:

Risk: <one clear sentence describing the risk>. Impact: <one clear sentence describing the potential impact>.

Examples:
Input: "Liquidity risk in forex trading"
Output:
Risk: Insufficient liquidity in forex trading may hinder trade execution at favorable prices. Impact: This can result in financial losses and reduced trading efficiency.

Input: "Credit risk in lending"
Output:
Risk: Borrowers may default on repayment obligations. Impact: This can cause financial losses and weaken lender stability.

Now process this input:
Input: "{text}"
Output:
"""
