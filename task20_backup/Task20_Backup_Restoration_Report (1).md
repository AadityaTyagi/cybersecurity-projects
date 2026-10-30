# Task 20: The Backup That Cannot Be Restored
**Author:** Aaditya TYagi
**Date:** 30-11-2026
**Implementation:** Python 3 (`backup_verify.py`)

## 1. Scenario and assumptions

**Fictional business:** A small accounting and bookkeeping company with 8 employees.

The company stores client records, invoices, receipts and monthly reports. It performs nightly backups of its important working files. The task scenario says backups have not previously been tested for restoration.

The following details are planning assumptions because the task brief does not specify a real business or backup system:

| Item | Assumption |
|---|---|
| Business | Small accounting and bookkeeping company with 8 employees |
| Critical data | Client records, invoices, receipts, accounting spreadsheets and reports |
| Backup method/location | Nightly encrypted backup to a separate cloud backup account, with a second offline copy retained |
| Backup owner | IT administrator; business owner approves recovery priorities |
| Target RPO | 24 hours maximum data loss |
| Target RTO | 8 business hours to restore essential files and resume core work |

The actual organization should confirm these targets based on business needs and legal obligations.

## 2. What to test

All tests must use a separate test location and synthetic or approved copies, never the live production folder.

| ID | Test | Safe method | Success criteria | Frequency |
|---|---|---|---|---|
| T1 | Single-file restore | Restore one sample invoice into an isolated folder | File opens and SHA-256 matches the trusted manifest | Monthly |
| T2 | Full-folder restore | Restore a sample client folder and its subfolders | All expected files are present and hashes match | Quarterly |
| T3 | Corruption and missing-file detection | Use the supplied demo to alter one restored file and remove another | Verification reports the corrupted and missing files | Quarterly |
| T4 | Older-version restore | Restore a previous approved version of a synthetic file | Correct version is recovered and its contents are usable | Quarterly |
| T5 | Access and permissions | Restore to a test account and check authorized access | Only approved users can access the restored data | Quarterly |
| T6 | Recovery-time test | Time a representative restore of test data | Essential data is restored within the 8-business-hour target | Quarterly |

## 3. Defining success

A restoration test is successful only when all relevant checks pass:

1. **Integrity:** SHA-256 hashes match the trusted manifest for every expected file.
2. **Completeness:** No expected files or folders are missing.
3. **Usability:** Sample documents open correctly and can be read by the intended application.
4. **Permissions:** Access is limited to authorized users.
5. **Recovery time:** Essential data is restored within the target RTO.
6. **Recovery point:** The restored version is no older than the agreed RPO.

A matching hash alone is not enough. A backup could faithfully contain a file that was already corrupted, encrypted by ransomware, incomplete or unusable before the backup was created. Therefore, restoration must also include content, application and business-user checks.

## 4. Safe testing rules

- Restore backups into a dedicated test folder or isolated test machine.
- Never restore test data over live production files.
- Use synthetic data first; obtain approval before using any real business data.
- Restrict access to the test environment to the IT administrator and approved testers.
- Keep the original backup unchanged during testing.
- Record the backup date, restore date, operator, files tested, results and any errors.
- Obtain approval from the business owner before a production recovery.
- Protect manifests and backup credentials; do not store passwords or secret keys in the report.

## 5. Contingencies

| Failure | Possible causes | Response |
|---|---|---|
| Backup corrupted | Storage failure, incomplete transfer, malware or damaged media | Isolate the damaged copy, preserve evidence, try another known-good backup, verify it before use and investigate the cause. |
| Backup inaccessible | Lost credentials, network outage, vendor outage or permission problem | Contact the authorized administrator or provider, use the documented account-recovery process and retrieve the separate offline copy if necessary. |
| Backup missing or too old | Failed scheduled job, retention issue or monitoring failure | Locate another backup, assess the data-loss period against the RPO, notify the business owner and recreate the backup schedule after recovery. |
| Backups encrypted by ransomware | Compromised systems or connected backup credentials | Isolate affected systems and backup connections, preserve evidence, do not reconnect potentially infected devices, and recover from a protected offline or immutable known-good copy after checking it. |

## 6. Ongoing process and ownership

- **Every night:** Automated backup job runs and records success or failure.
- **Every morning:** IT administrator reviews backup-job alerts and investigates failures.
- **Monthly:** Restore a single sample file and verify its hash and usability.
- **Quarterly:** Perform a full-folder restore, older-version test, permissions check and recovery-time test.
- **After major system changes:** Repeat relevant restore tests.
- **Sign-off:** IT administrator records evidence; business owner reviews and approves the test result.
- **Escalation:** Any failed test is treated as an issue. The administrator records the cause, assigns an owner and deadline, and repeats the test after remediation.

## 7. Evidence from the Python demonstration

The supplied `backup_verify.py` script creates synthetic invoice files and a client CSV file. It builds a manifest containing each file's relative path, SHA-256 hash and size. It then copies the sample data to a restore directory and compares the restored files with the manifest.

### Test A: Clean restore

**Actual output supplied:**
```text
--- Test A: clean restore ---
Verified OK : 6/6
Restore time: 0.001s
RESULT: PASS
```

**Interpretation:** All six expected files were found and their SHA-256 hashes matched the manifest. The clean synthetic restore passed the script's checks.

### Test B: Corrupted and missing file

**Actual output supplied:**
```text
--- Test B: corrupted + missing file ---
Verified OK : 4/6
Corrupted   : ['invoices/inv_2.txt']
Missing     : ['clients.csv']
RESULT: FAIL
```

**Interpretation:** The script detected that `invoices/inv_2.txt` had been modified and that `clients.csv` was missing. The test correctly reported failure because the restored copy was not complete and unchanged.

### What the demonstration proves—and does not prove

The demonstration shows that a manifest-based SHA-256 comparison can identify changed and missing files in this synthetic restore. It does not prove that a real business backup is available, malware-free, application-consistent, correctly permissioned or recoverable within the target RTO. Those require separate tests.

**Implementation note:** The current `report()` function determines PASS/FAIL from corrupted and missing files. It lists unexpected extra files but does not currently make them fail the test. If the business requires an exact file-set match, update the success condition to include `res["unexpected"]`.

## 8. Conclusion

A backup is not proven reliable simply because a scheduled job reports success. It must be restored and checked. This project demonstrates a safe validation approach using a file manifest, SHA-256 hashes and synthetic restore tests.

The clean restore passed with all six files verified. The deliberately damaged restore failed and identified one corrupted file and one missing file. These results demonstrate why regular restoration tests, clear success criteria, documented ownership and recovery contingencies are necessary.

The proposed business plan adds checks for completeness, usability, permissions, recovery time and recovery point. These checks provide stronger evidence that the business can actually recover its important data.

## 9. References

Only include sources you have actually opened and read. Useful starting points:

- NIST, **SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems** — https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
- CISA, **StopRansomware Guide** — https://www.cisa.gov/stopransomware/ransomware-guide
- Python documentation, **`hashlib` — Secure hashes and message digests** — https://docs.python.org/3/library/hashlib.html
- Python documentation, **`shutil` — High-level file operations** — https://docs.python.org/3/library/shutil.html
