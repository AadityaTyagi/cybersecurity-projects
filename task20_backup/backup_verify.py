"""Task 20 helper: build a hash manifest of source data, then verify a restored copy.
Usage:
  python backup_verify.py manifest <source_dir> <manifest.json>
  python backup_verify.py verify <manifest.json> <restored_dir>
  python backup_verify.py demo        # synthetic end-to-end run
"""
import hashlib, json, os, shutil, sys, tempfile, time

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(8192), b""):
            h.update(c)
    return h.hexdigest()

def build_manifest(src):
    m = {}
    for root, _, files in os.walk(src):
        for fn in files:
            p = os.path.join(root, fn)
            m[os.path.relpath(p, src)] = {"sha256": sha256_file(p), "size": os.path.getsize(p)}
    return m

def verify(manifest, restored):
    ok, bad, missing = [], [], []
    for rel, meta in manifest.items():
        p = os.path.join(restored, rel)
        if not os.path.exists(p): missing.append(rel)
        elif sha256_file(p) != meta["sha256"]: bad.append(rel)
        else: ok.append(rel)
    present = {os.path.relpath(os.path.join(r, f), restored) for r, _, fs in os.walk(restored) for f in fs}
    extra = sorted(present - set(manifest))
    return {"ok": ok, "corrupted": bad, "missing": missing, "unexpected": extra}

def report(res, seconds=None):
    total = len(res["ok"]) + len(res["corrupted"]) + len(res["missing"])
    print(f"Verified OK : {len(res['ok'])}/{total}")
    for k in ("corrupted", "missing", "unexpected"):
        if res[k]: print(f"{k.capitalize():12}: {res[k]}")
    if seconds is not None: print(f"Restore time: {seconds:.3f}s")
    passed = not (res["corrupted"] or res["missing"])
    print("RESULT:", "PASS" if passed else "FAIL")
    return passed

def demo():
    tmp = tempfile.mkdtemp(); src = os.path.join(tmp, "source"); os.makedirs(src + "/invoices")
    for i in range(5):
        open(f"{src}/invoices/inv_{i}.txt", "w").write(f"synthetic invoice {i}\n" * 50)
    open(f"{src}/clients.csv", "w").write("id,name\n1,Test Client\n")
    manifest = build_manifest(src)
    print("--- Test A: clean restore ---")
    t = time.time(); r = os.path.join(tmp, "restoreA"); shutil.copytree(src, r)
    report(verify(manifest, r), time.time() - t)
    print("\n--- Test B: corrupted + missing file ---")
    r2 = os.path.join(tmp, "restoreB"); shutil.copytree(src, r2)
    open(f"{r2}/invoices/inv_2.txt", "ab").write(b"x")
    os.remove(f"{r2}/clients.csv")
    report(verify(manifest, r2))
    shutil.rmtree(tmp)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["manifest"]:
        json.dump(build_manifest(a[1]), open(a[2], "w"), indent=2); print("Wrote", a[2])
    elif a[:1] == ["verify"]:
        sys.exit(0 if report(verify(json.load(open(a[1])), a[2])) else 1)
    elif a[:1] == ["demo"]: demo()
    else: print(__doc__)
