# Cybersecurity Assessment: Tasks 20 and 12

- `task20_backup/` : backup and restoration test plan (`task20_backup_plan.md`) and `backup_verify.py` (hash manifest + restore verifier)
- `task12_hashing/` : hashing demo (`hash_demo.py`) and write-up (`task12_writeup.md`)

## Run
```
python3 task12_hashing/hash_demo.py
python3 task20_backup/backup_verify.py demo
```
Python 3.8+ standard library only. All data is synthetic.

## Link between the tasks
Task 20 uses SHA-256 manifests (Task 12) to prove restored files match the originals.
