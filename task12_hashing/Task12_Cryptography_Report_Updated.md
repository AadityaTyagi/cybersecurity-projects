# Task 12: Explore a Cryptography Concept --- Hashing

**Author:** Aaditya Tyagi
**Date:** 30-10-2026
**Programming language:** Python\
**Concept explored:** Cryptographic hashing, with SHA-256 as the main
example

------------------------------------------------------------------------

## 1. Introduction

Cryptography helps protect information and communications. This project
explores **cryptographic hashing**, focusing on the SHA-256 hash
function.

A hash function takes input data and produces a fixed-length output
called a *hash* or *digest*. SHA-256 produces a 256-bit digest, normally
displayed as 64 hexadecimal characters.

A cryptographic hash function is designed to be deterministic (the same
input gives the same output), one-way (it is not designed to recover the
original input), and resistant to finding two different inputs with the
same digest (collision resistance).

The purpose of this project is to demonstrate how hashes can help detect
changes to data, and to explain why a hash by itself does not provide
every kind of security.

## 2. Objectives

-   Generate SHA-256 hashes for files.
-   Demonstrate that identical input produces an identical hash.
-   Observe the avalanche effect when a small input change is made.
-   Use a hash comparison to detect a changed copy of a file.
-   Demonstrate why a hash alone does not prove authenticity.
-   Compare plain SHA-256 with salted scrypt for a password example.
-   Compare the output of MD5, SHA-1, SHA-256 and SHA3-256.

## 3. Tools and technologies

-   **Python 3**
-   **hashlib:** provides hash algorithms and the scrypt password-based
    key derivation function.
-   **hmac:** creates a keyed message authentication code.
-   **os:** supports file paths and random salt generation.
-   **shutil:** copies the demonstration file.
-   **tempfile:** creates a temporary directory for the sample files.

The demonstration uses synthetic text and temporary files. It does not
access or modify real business data.

## 4. How the program works

The main function creates a temporary text file containing:

`Quarterly report: balance is 1000`

The `sha256_file(path)` function:

1.  Creates a SHA-256 hash object.
2.  Opens the file in binary mode.
3.  Reads the file in chunks of 8192 bytes.
4.  Adds each chunk to the hash object.
5.  Returns the final digest as a hexadecimal string.

Reading in chunks allows the function to process files without loading
the entire file into memory at once.

The `bit_diff(a_hex, b_hex)` function converts two hexadecimal digests
to integers, applies XOR, and counts the number of set bits. This
measures how many bit positions differ between the two hash values.

The program runs six main demonstrations, followed by an additional experiment with files of different sizes.

## 5. Practical demonstration and observations

### 5.1 Deterministic, fixed-length output

The program hashes the same original file twice.

**Observed result:** Both runs produced:

`d74bf24d47ee79f7442ee759c2a252cfd07adee94a5d52e126b111561561e6a0`

The program reported `Same? True` and `Length: 256 bits`.

**Explanation:** SHA-256 is deterministic: the same file contents
produce the same digest. The digest length is fixed at 256 bits,
regardless of the input file's size.

### 5.2 Avalanche effect

The program creates a second file with one changed digit:

-   Original: `Quarterly report: balance is 1000`
-   Modified: `Quarterly report: balance is 9000`

**Observed result:** The original and modified digests were different.
In the latest run shown in the VS Code screenshot, **131 of 256 bits** differed. The earlier sample output records 117 bits; this difference is expected because the exact bit count depends on the tested input pair and run.

**Explanation:** A small change to the input caused a large,
unpredictable-looking change in the output. This illustrates the
avalanche effect, a desirable property of cryptographic hash functions.
The exact number of differing bits can vary with the input; 117 is the
result of this particular run.

### 5.3 Integrity check on a copy

The program copies the original file and compares the copy's SHA-256
digest with the original digest. It then appends one space to the copy
and checks again.

**Observed result:** - Before the extra space:
`Copy matches original? True` - After the extra space:
`After corruption, matches? False`

**Explanation:** Matching digests provide evidence that the file
contents match the reference file. Adding a space changes the file
contents and therefore changes its digest. This is a simple
demonstration of using hashes for file-integrity checking.

### 5.4 A hash alone does not prove authenticity

The program simulates an attacker changing the report and publishing a
new hash for the altered content. It also generates an HMAC using a
demonstration secret key.

**Observed result:** The altered file has a valid SHA-256 digest for its
altered contents. The program explains that a verifier who receives both
the altered file and the attacker's replacement hash could see a
matching pair.

**Explanation:** A plain hash can help detect accidental or unauthorized
changes only when the expected hash comes from a trusted source. If an
attacker can replace both the file and the reference hash, a simple hash
comparison does not establish who supplied the file. HMAC addresses this
different problem by using a shared secret key to authenticate a
message, provided the key remains secret and is securely managed.

### 5.5 Plain SHA-256 compared with salted scrypt

The program uses a synthetic password string in a demonstration. It
first calculates a plain SHA-256 digest. It then generates two random
salts and derives two scrypt outputs using those different salts.

**Observed result:** Plain SHA-256 gives the same digest for the same
password input. The two scrypt outputs differ because each run uses a
different random salt.

**Explanation:** SHA-256 is designed to be fast, which makes it
unsuitable as the sole password-storage method. Password storage should
use a password-hashing or key-derivation function designed to make
guessing more expensive, with a unique salt for each password. This
demonstration uses scrypt to illustrate the idea.

**Safety note:** The password in the script is only synthetic
demonstration data. Do not use it as a real password. A real system must
securely store the salt and derived password hash, use appropriate
parameters, and implement verification correctly.

### 5.6 Algorithm comparison

The program calculates digests for the same input, `hello`, using MD5,
SHA-1, SHA-256 and SHA3-256.

**Observed output:**

  --------------------------------------------------------------------------------------------------------
  Algorithm                           Digest shown by the program
  ----------------------------------- --------------------------------------------------------------------
  MD5                                 `5d41402abc4b2a76b9719d911017c592`

  SHA-1                               `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d`

  SHA-256                             `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`

  SHA3-256                            `3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392`
  --------------------------------------------------------------------------------------------------------

**Explanation:** Different algorithms produce different digest values
and, in some cases, different digest lengths. The script notes that MD5
and SHA-1 have known practical collision attacks and should not be
selected for security-sensitive collision-resistance requirements.
SHA-256 and SHA3-256 are modern hash functions standardized by NIST.

## 6. What hashing can and cannot protect

  -----------------------------------------------------------------------
  Hashing can help with               Hashing alone does not provide
  ----------------------------------- -----------------------------------
  Detecting whether file contents     Encryption or confidentiality
  differ from a trusted reference     

  Checking that two files have        Proof of the sender's identity
  matching contents with overwhelming 
  confidence                          

  Supporting digital-signature        A digital signature by itself
  systems                             

  Supporting secure password-storage  Safe password storage when a fast
  designs when an appropriate         general-purpose hash is used alone
  password-hashing function is used   

  Detecting accidental corruption     Protection against an attacker who
  when the expected digest is         can replace both the file and its
  trustworthy                         reference hash
  -----------------------------------------------------------------------

A hash is not encryption: it is not designed to be reversed to recover
the original data. Also, a matching hash does not by itself prove that a
file came from a particular person or organization.

## 7. Real-world uses

-   **File integrity:** A downloaded file can be hashed and compared
    with a digest published through a trusted channel.
-   **Password storage:** Systems can store password-derived values
    using password-hashing functions such as scrypt, with unique salts,
    rather than storing plaintext passwords.
-   **Digital signatures:** Hashes are used as part of digital-signature
    processes. The signature and trusted public key provide authenticity
    and integrity checks; a hash alone is not a signature.
-   **Backups:** A backup file can be hashed and compared with a trusted
    digest to help detect changes or corruption. This connects to Task
    20, where restoration tests should also confirm that recovered files
    are usable and complete.

## 8. Additional experiment: Different file sizes

The program creates two temporary files: a small file containing `Hello Python!` and a larger file containing the same phrase repeated 10,000 times. It calculates the SHA-256 digest length for each file.

**Observed result from the latest VS Code run:**

- Small file size: **13 bytes**
- Large file size: **140,000 bytes**
- Small file digest length: **256 bits**
- Large file digest length: **256 bits**
- Program check: `Both are 256 bits: True`

**Explanation:** The input files have very different sizes, but SHA-256 produces a fixed-size 256-bit digest for both. This demonstrates that SHA-256 output length does not depend on input size.

## 9. Limitations and considerations

1.  **No confidentiality:** Hashing does not hide the input. Use
    encryption when data must remain secret.
2.  **No recovery:** A hash is not intended to be reversed to
    reconstruct the original input.
3.  **No identity proof by itself:** A plain digest does not identify
    who created or sent the data.
4.  **Trusted reference required:** A file hash comparison is only
    useful for authenticity-related decisions when the expected digest
    is obtained through a trustworthy channel.
5.  **Password hashing needs special care:** Fast general-purpose hashes
    such as SHA-256 are not appropriate alone for password storage. Use
    a dedicated password-hashing function with a unique salt and
    suitable parameters.
6.  **Collisions are theoretically possible:** A collision means two
    different inputs have the same digest. SHA-256 is designed to make
    finding such collisions computationally infeasible, but no
    finite-length hash can make collisions mathematically impossible.
7.  **A hash does not prevent changes:** It can help detect changes when
    compared with a trusted digest, but it does not stop someone from
    modifying a file.

## 10. Conclusion

This project demonstrated how SHA-256 produces a deterministic,
fixed-length digest and how even a small change in file contents changes
the digest. The file-copy experiment showed how comparing a file's hash
with a trusted reference can help detect corruption or modification.

The authenticity experiment showed that a hash alone cannot prove who
created a file, while the HMAC example introduced the use of a secret
key for message authentication. The password experiment showed why a
fast hash such as SHA-256 should not be used alone for password storage,
and why a salted password-hashing function such as scrypt is more
appropriate.

Overall, cryptographic hashing is useful for integrity checks and as a
building block in security systems, but it must be combined with other
controls to provide confidentiality, authentication and secure password
storage.


1.  **Full terminal screenshot:** Shows the deterministic output,
    avalanche effect, integrity check, authenticity/HMAC example,
    password-hashing comparison, algorithm comparison, and additional
    different-file-size experiment.

Keep the original screenshot file in the project's `screenshots/`
folder. If the evaluator prefers larger text, you may also add separate
close-up screenshots of the terminal sections.



## 12. References

-   NIST, **FIPS PUB 180-4: Secure Hash Standard** ---
    https://csrc.nist.gov/pubs/fips/180-4/upd1/final
-   NIST, **FIPS PUB 202: SHA-3 Standard** ---
    https://csrc.nist.gov/pubs/fips/202/final
-   OWASP, **Password Storage Cheat Sheet** ---
    https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
-   Python documentation, **`hashlib` --- Secure hashes and message
    digests** --- https://docs.python.org/3/library/hashlib.html
-   Python documentation, **`hmac` --- Keyed-Hashing for Message
    Authentication** --- https://docs.python.org/3/library/hmac.html

------------------------------------------------------------------------

## Submission check


