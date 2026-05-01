# Week 2 Day 5 — AI Quality Review

## Objective
Evaluate AI response quality across endpoints using 10 fresh prompts.
Measure:
- Accuracy
- Relevance
- Completeness
- Clarity

Target average score: >= 4/5


---

# Test Results

| # | Endpoint | Input Prompt | Response Summary | Score (/5) | Notes |
|---|-----------|--------------|------------------|-------------|-------|
| 1 | /query | What is Artificial Intelligence? | Correct explanation of AI concepts | 5 | Accurate and clear |
| 2 | /query | Explain machine learning in simple words | Simple and understandable response | 5 | Beginner-friendly |
| 3 | /query | What are neural networks? | Good technical explanation | 4 | Could include examples |
| 4 | /query | Difference between AI and ML | Correct comparison provided | 5 | Well structured |
| 5 | /query | What is deep learning? | Accurate explanation | 4 | Slightly brief |
| 6 | /query | Explain Generative AI | Correct overview with examples | 5 | Relevant response |
| 7 | /query | What is ChromaDB? | Correct vector DB explanation | 4 | Could be more detailed |
| 8 | /query | What is Redis cache? | Accurate caching explanation | 5 | Clear and concise |
| 9 | /query | Explain FastAPI | Correct backend framework explanation | 4 | Needed more examples |
|10 | /query | What is API latency? | Correct explanation of response delays | 5 | Very clear |

---

# Average Score

Total Score = 46

Average Accuracy Score:

46 / 10 = 4.6 / 5

✅ Target achieved (>= 4/5)

---

# Failing Prompt Improvements

## Original Prompt
"Explain AI"

### Problem
Too broad and generic.

### Improved Prompt
"Explain Artificial Intelligence with real-world examples in simple words."

---

## Original Prompt
"What is ML?"

### Problem
Very short and lacks context.

### Improved Prompt
"Explain Machine Learning for beginners with examples."

---

# Final Observation

The AI system performed consistently across all tested inputs.
Responses were relevant, technically correct, and context-aware.

Strengths:
- Fast response generation
- Accurate technical explanations
- Good contextual understanding

Areas for improvement:
- Add more detailed examples
- Improve explanation depth for technical topics