# Lesson: phases/00-setup-and-tooling/08-editor-setup/docs/en.md
# Exercise 3: Check Pylance hints and Black formatting.
# Reference: https://code.visualstudio.com/docs/python/formatting
# Run: python editor_practice.py


def greet(name: str) -> str:
    return f"Hello, {name}!"


message = greet("Kevin")
print(message)
