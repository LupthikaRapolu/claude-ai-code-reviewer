def review_code_prompt(code):
    return f"""
You are a senior software engineer performing a professional code review.

Analyze the following code and provide:

1. Bugs or errors
2. Performance improvements
3. Security concerns
4. Code quality suggestions
5. A refactored version

Code:
{code}
"""

def explain_code_prompt(code):
    return f"""
You are a software engineer explaining code to a junior developer.

Explain the following code step by step in simple terms.

Code:
{code}
"""


def generate_tests_prompt(code):
    return f"""
You are a QA engineer.

Generate unit tests for the following code.

Include edge cases and explain why each test is important.

Code:
{code}
"""


def improve_code_prompt(code):
    return f"""
You are a senior software engineer.

Improve the following code for:
- readability
- performance
- maintainability

Return an improved version with explanations.

Code:
{code}
"""