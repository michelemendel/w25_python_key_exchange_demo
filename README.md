# W25 Python Final Project - Key Exchange Demo

This project demonstrates the Diffie-Hellman key exchange algorithm, which allows two parties to establish a shared secret key over an insecure channel.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Node.js (for running the presentation)

## Setup

1. Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Running the Demo

```bash
python demo_runner.py
or
./demo_runner.py
```

The program will guide you through each step of the key exchange process, waiting for you to press Enter to continue to the next step.

## Run presentation

For installation instructions, see the [Slidev documentation](https://sli.dev/guide/getting-started.html).

To run the presentation using Slidev:

```bash
slidev presentation/slides.md
```

## Technology used

### Python Program

- **Python 3.8+** - Main programming language for the cryptographic implementation
- **SymPy** - Python library for symbolic mathematics, used for prime number generation and primality testing
- **Cryptography** - Python library providing cryptographic recipes and primitives, used for AES encryption/decryption
- **AES-256-CBC** - Advanced Encryption Standard used for message encryption/decryption
- **HKDF** - HMAC-based Key Derivation Function for deriving AES keys from shared secrets
- **Diffie-Hellman Key Exchange** - Cryptographic protocol for secure key establishment

### Presentation

- **Slidev** - Vue.js-based presentation framework for creating slides
- **Node.js** - JavaScript runtime for running the presentation development server
