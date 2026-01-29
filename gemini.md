# Gemini - Project Constitution

## Data Schemas

### Payload Schema (Internal)
```json
{
  "source_code": "String (Selenium Java)",
  "framework": "TestNG",
  "target_language": "TypeScript | JavaScript",
  "metadata": {
    "filename_hint": "String",
    "timestamp": "ISO8601"
  }
}
```

### Output Schema
```json
{
  "converted_code": "String (Playwright)",
  "status": "success | error",
  "conversion_logs": ["String"],
  "output_path": "String (Relative path to created file)"
}
```

## Behavioral Rules
1. **Rule 1**: Always follow the B.L.A.S.T. protocol.
2. **Rule 2**: No scripts in `tools/` until Phase 1 requirements are met.

## Architectural Invariants
- 3-Layer Architecture (Architecture, Navigation, Tools).
