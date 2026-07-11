# Technical Debt

This document tracks improvements that have been intentionally postponed.

The goal is to keep development moving while ensuring good ideas are not forgotten.

---

## High Priority

_None_

---

## Medium Priority

_None_

---

## Low Priority

### CSV Reader

**Improvement**

Refactor repeated `pd.read_csv()` calls into a private helper method.

Current:

```python
pd.read_csv(...)
```

Future:

```python
def _read_csv(...):
```

Reason

Reduce duplicated code and centralize CSV reading options.

Status

Backlog

---

### Shared ID Generator

Create a reusable ID generator.

Current

WorkspaceService

DatasetRegistry

Future

```
app/utils/id_generator.py
```

Reason

Avoid duplicate ID generation logic.

Status

Backlog

---

### Logging

Introduce centralized logging.

Future

```
app/core/logger.py
```

Reason

Replace print statements and improve debugging.

Status

Backlog

## Temporary File Cleanup

**Current**

Temporary file deletion is disabled on Windows because the file may still be locked by openpyxl/pandas.

**Future**

Implement a retry-based cleanup mechanism or redesign the upload pipeline so the temporary file is deleted safely after processing.

**Priority**

Medium

**Status**

Backlog