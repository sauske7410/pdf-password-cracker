import itertools
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, Optional

import pikepdf
from tqdm import tqdm


def generate_passwords(chars: str, min_length: int, max_length: int) -> Iterable[str]:
    for length in range(min_length, max_length + 1):
        for tup in itertools.product(chars, repeat=length):
            yield ''.join(tup)


def load_passwords(wordlist_file: str) -> Iterable[str]:
    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            pwd = line.strip()
            if pwd:
                yield pwd


def try_password(pdf_file: str, password: str) -> Optional[str]:
    try:
        with pikepdf.open(pdf_file, password=password):
            return password
    except pikepdf._core.PasswordError:
        return None
    except Exception:
        return None


def decrypt_pdf(pdf_file: str, password_source: Iterable[str], max_workers: int = 4, total: Optional[int] = None) -> Optional[str]:
    password_iter = iter(password_source)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for _ in range(max_workers):
            try:
                pwd = next(password_iter)
            except StopIteration:
                break
            futures[executor.submit(try_password, pdf_file, pwd)] = pwd

        if not futures:
            return None

        with tqdm(total=total, desc="Decrypting PDF", unit="password", dynamic_ncols=True) as pbar:
            while futures:
                for future in as_completed(list(futures.keys())):
                    pwd = futures.pop(future)
                    result = future.result()
                    pbar.update(1)

                    if result:
                        executor.shutdown(cancel_futures=True)
                        return result
                    try:
                        next_pwd = next(password_iter)
                        futures[executor.submit(try_password, pdf_file, next_pwd)] = next_pwd
                    except StopIteration:
                        pass

    return None


if __name__ == "__main__":
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(description="Optimized PDF password cracker")
    parser.add_argument("pdf_file", help="Path to the password-protected PDF file")
    parser.add_argument("--wordlist", help="Path to the password list file")
    parser.add_argument("--g", action="store_true", help="Generate passwords on the fly")
    parser.add_argument("--min", type=int, default=1, help="Minimum length (generator)")
    parser.add_argument("--max", type=int, default=3, help="Maximum length (generator)")
    parser.add_argument("--c", type=str, default=string.ascii_letters + string.digits,
                        help="Characters to use (generator)")
    parser.add_argument("--max_workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--count", action="store_true", help="Count total candidates (slower)")

    args = parser.parse_args()

    if not os.path.isfile(args.pdf_file):
        print("[-] PDF file not found.")
        sys.exit(1)

    total = None
    if args.g:
        password_source = generate_passwords(args.c, args.min, args.max)
        if args.count:
            charset_size = len(args.c)
            total = sum(charset_size ** L for L in range(args.min, args.max + 1))
    elif args.wordlist:
        if not os.path.isfile(args.wordlist):
            print("[-] Wordlist file not found.")
            sys.exit(1)
        password_source = load_passwords(args.wordlist)
        if args.count:
            with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                total = sum(1 for line in f if line.strip())
            password_source = load_passwords(args.wordlist)
    else:
        print("[-] Either --wordlist or --g must be specified.")
        sys.exit(1)

    found = decrypt_pdf(args.pdf_file, password_source, args.max_workers, total)
    if found:
        print(f"[+] Password found: {found}")
    else:
        print("[-] Unable to decrypt PDF. Password not found.")
