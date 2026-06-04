---
name: test-and-verify
description: Run full test suite and verify all 117 tests pass with zero deprecation warnings
triggers:
  - "/test"
  - "/verify"
  - "run tests"
inputs:
  verbose: false
exit_criteria:
  - "All 117 tests pass"
  - "Zero DeprecationWarning errors"
---

# Test & Verify Workflow

## Phase 1: Run Tests
Run the full test suite:

```bash
cd frk
pytest tests/ -v -W error::DeprecationWarning
```

Check exit code. If non-zero, proceed to Phase 2. If zero, report success.

## Phase 2: Diagnose Failures
Identify which tests failed and why. Check:
1. Are imports correct?
2. Are the expected values matching actual outputs?
3. Are there any deprecation warnings?

Fix the issues and re-run Phase 1.

## Phase 3: Final Verification
Confirm:
- `pytest tests/ -v -W error::DeprecationWarning` exits with code 0
- 117/117 tests pass
- No DeprecationWarning in output
- Masumi and Featherless files are untouched
- No credit/securitisation references introduced
