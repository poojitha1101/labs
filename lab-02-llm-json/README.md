# Lab 02: LLM JSON Output 🤖

**Points: 20 | Time: ~1 hour**

## Problem
Write a function that takes a plain text article and returns a structured JSON summary (no actual LLM call required — simulate the behavior).

## Your Task
Implement `summarize_text(text)` in `solution.py`.

## Requirements
- Input: any string of text
- Output: a Python `dict` with exactly these keys:
  - `"title"` — a 5-word max summary title (string)
  - `"points"` — a list of 3 key points (list of 3 strings)
  - `"sentiment"` — one of: `"positive"`, `"neutral"`, `"negative"` (string)

## How to Test Locally
```bash
pytest tests/
```
