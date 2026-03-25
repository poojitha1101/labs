# Lab 03: TOON Converter 🔄

**Points: 20 | Time: ~1 hour**

## Problem
TOON (Token-Oriented Object Notation) represents arrays of JSON objects as a header row + data rows — similar to CSV, but for JSON.

## Your Task
Implement `json_to_toon(data)` in `solution.py`.

## TOON Format
```
# fields: id, name, score
1 | Alice | 92
2 | Bob | 87
```

## Requirements
- Input: a **list of dicts** (all with same keys).
- Output: a **string** in the TOON format:
  - First line: `# fields: key1, key2, key3`
  - Remaining lines: `val1 | val2 | val3` for each row
- Also implement `count_tokens(text)` → returns `len(text.split())` as a proxy for token count.
