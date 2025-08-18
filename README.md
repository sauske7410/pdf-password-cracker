# pdf-password-cracker
A fast, memory‑efficient Python utility to attempt user‑password decryption of PDFs using either a wordlist or on‑the‑fly generation.

Use only on files owned or explicitly authorized for testing.

Features
Wordlist mode and generator (brute‑force) mode

Multithreaded, early stop on success

Streams candidates (no massive preloading)

Optional accurate progress totals

Requirements
Python 3.8+

pip install pikepdf tqdm

Quick Start
Wordlist:

python -u ".\cracker.py" ".\secret.pdf" --wordlist ".\rockyou.txt" --max_workers 8

Generator:

python -u ".\cracker.py" ".\secret.pdf" --g --min 1 --max 4 --c 1234567890 --max_workers 8

macOS/Linux:

python3 -u "./cracker.py" "./secret.pdf" --wordlist "./rockyou.txt" --max_workers 8

python3 -u "./cracker.py" "./secret.pdf" --g --min 1 --max 4 --c 1234567890 --max_workers 8

CLI Options
pdf_file: Path to the protected PDF

--wordlist PATH: Use a wordlist file (one password per line)

--g: Generate passwords on the fly (mutually exclusive with --wordlist)

--min INT: Minimum length (generator)

--max INT: Maximum length (generator)

--c STR: Characters for generator (e.g., 0123456789 or abcdef)

--max_workers INT: Parallel threads

--count: Show total progress (slower; optional)

Examples
Generator, digits 1–4 chars:

python -u ".\cracker.py" ".\ex3.pdf" --g --min 1 --max 4 --c 1234567890

Generator, lowercase 1–4 chars:

python -u ".\cracker.py" ".\ex3.pdf" --g --min 1 --max 4 --c abcdef

Wordlist, 8 workers:

python -u ".\cracker.py" ".\ex3.pdf" --wordlist ".\rockyou.txt" --max_workers 8

Wordlist with total count:

python -u ".\cracker.py" ".\ex3.pdf" --wordlist ".\custom.txt" --count

Generator, mixed set, more threads:

python -u ".\cracker.py" ".\ex3.pdf" --g --min 2 --max 6 --c abcdef0123 --max_workers 12

Tips
Validate quickly with a tiny search space:

python -u ".\cracker.py" ".\ex3.pdf" --g --min 1 --max 2 --c 01

Start with targeted wordlists before brute‑force.

Increase --max_workers gradually based on CPU.

VS Code Usage
Run from the integrated terminal:

py -u ".\cracker.py" ".\ex3.pdf" --g --min 1 --max 4 --c 1234567890

py -u ".\cracker.py" ".\ex3.pdf" --wordlist ".\lists\top1000.txt" --max_workers 8

Optional: Add a launch configuration (Run and Debug → create launch.json):

Wordlist

program: ${workspaceFolder}/cracker.py

args: ["${workspaceFolder}/ex3.pdf", "--wordlist", "${workspaceFolder}/rockyou.txt", "--max_workers", "8"]

Generator

program: ${workspaceFolder}/cracker.py

args: ["${workspaceFolder}/ex3.pdf", "--g", "--min", "1", "--max", "4", "--c", "1234567890", "--max_workers", "8"]

Legal
For lawful, authorized use only. The author assumes no responsibility for misuse.
