"""Task 12 demo: hashing, integrity, and its limits. Uses only synthetic data."""
import hashlib, hmac, os, shutil, tempfile

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def bit_diff(a_hex, b_hex):
    x = int(a_hex, 16) ^ int(b_hex, 16)
    return bin(x).count("1")

def main():
    tmp = tempfile.mkdtemp()
    a = os.path.join(tmp, "original.txt")
    with open(a, "w") as f:
        f.write("Quarterly report: balance is 1000\n")

    print("== 1. Deterministic, fixed-length output ==")
    h1, h2 = sha256_file(a), sha256_file(a)
    print("Run 1:", h1); print("Run 2:", h2); print("Same?", h1 == h2)
    print("Length:", len(h1) * 4, "bits")

    print("\n== 2. Avalanche effect (change 1 character) ==")
    b = os.path.join(tmp, "modified.txt")
    with open(b, "w") as f:
        f.write("Quarterly report: balance is 9000\n")
    hb = sha256_file(b)
    print("Original:", h1); print("Modified:", hb)
    print(f"Bits differing: {bit_diff(h1, hb)} / 256")

    print("\n== 3. Integrity check on a copy (backup scenario) ==")
    c = os.path.join(tmp, "copy.txt"); shutil.copy(a, c)
    print("Copy matches original?", sha256_file(c) == h1)
    with open(c, "ab") as f:
        f.write(b" ")  # simulate silent corruption
    print("After corruption, matches?", sha256_file(c) == h1)

    print("\n== 4. LIMIT: hash alone does not prove authenticity ==")
    forged = b"Quarterly report: balance is 9000\n"
    print("Attacker alters file AND publishes a new hash:", hashlib.sha256(forged).hexdigest())
    print("-> Verifier sees a 'matching' hash. Integrity without a trusted source is not authenticity.")
    key = b"shared-secret-key"
    tag = hmac.new(key, forged, hashlib.sha256).hexdigest()
    print("HMAC needs a secret key an attacker lacks:", tag)

    print("\n== 5. LIMIT: fast hashes are weak for passwords ==")
    pw = b"Summer2024!"
    print("Plain SHA-256 (same every time, unsalted):", hashlib.sha256(pw).hexdigest())
    s1, s2 = os.urandom(16), os.urandom(16)
    k1 = hashlib.scrypt(pw, salt=s1, n=2**14, r=8, p=1).hex()
    k2 = hashlib.scrypt(pw, salt=s2, n=2**14, r=8, p=1).hex()
    print("scrypt + salt, run 1:", k1[:32] + "...")
    print("scrypt + salt, run 2:", k2[:32] + "...  (differs despite same password)")

    print("\n== 6. Algorithm comparison ==")
    for name in ("md5", "sha1", "sha256", "sha3_256"):
        print(f"{name:9}", hashlib.new(name, b"hello").hexdigest())
    print("Note: MD5 and SHA-1 have known practical collision attacks; avoid for security use.")
    print("\n== 7. Additional experiment ==")

    small = os.path.join(tmp, "small.txt")
    large = os.path.join(tmp, "large.txt")

    with open(small, "w") as f:
        f.write("Hello Python!")

    with open(large, "w") as f:
        f.write("Hello Python! " * 10000)

    h_small = sha256_file(small)
    h_large = sha256_file(large)

    print("Small file size:", os.path.getsize(small), "bytes")
    print("Large file size:", os.path.getsize(large), "bytes")
    print("Small hash length:", len(h_small) * 4, "bits")
    print("Large hash length:", len(h_large) * 4, "bits")
    print("Both are 256 bits:",
          len(h_small) == 64 and len(h_large) == 64)
    shutil.rmtree(tmp)

if __name__ == "__main__":
    main()
