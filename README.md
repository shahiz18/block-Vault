# block-Vault


# 🗄️ BlockVault

> **Secure • Decentralised • Auditable**
> Your files get Fort Knox treatment — no blockchain hype required.

---

## 📑 Table of Contents

1. [Why BlockVault?](#why-blockvault)
2. [Features](#features)
3. [Architecture Overview](#architecture-overview)
4. [Tech Stack](#tech-stack)
5. [Prerequisites](#prerequisites)
6. [Quick Start](#quick-start)
7. [Configuration](#configuration)
8. [Usage](#usage)
9. [Database Schema](#database-schema)
10. [Testing](#testing)
11. [Roadmap](#roadmap)
12. [Contributing](#contributing)
13. [License](#license)

---

## 🤔 Why BlockVault?

Typical cloud drives force you to trust the provider to:

* **Store** your files correctly.
* **Encrypt** them faithfully.
* **Never** snoop or lose data.

BlockVault flips that trust model:

* **Client‑side AES‑256 encryption** — only *you* hold the keys.
* **IPFS storage via Pinata** — decentralised, content‑addressed (the CID *is* the checksum).
* **Local audit log** — every upload (CID, filename, timestamp) is recorded in a SQL database you control.

Result: a tamper‑evident, zero‑knowledge file vault without the overhead of a blockchain. 🔐

---

## ✨ Features

* **End‑to‑end encryption** (Python `cryptography`, AES‑256‑GCM)
* **Decentralised storage** (IPFS through Pinata JWT API)
* **Auditability** via a **SQL database** (SQLite by default, PostgreSQL ready)
* **Flask REST API** + minimal HTML/CSS/JS frontend — no SPA bloat
* **Dockerised dev environment** *(optional)*
* **Modular design** — swap IPFS provider or database with minimal code changes

> **Status:** Core functionality (encryption + IPFS + DB logging) complete. 🏁

---

## 🏗️ Architecture Overview

```
   ┌──────────┐      Encrypt      ┌────────────┐     Store    ┌────────────┐
   │ Frontend │ ───────────────▶ │ Flask API  │ ───────────▶ │  Pinata/IPFS│
   └──────────┘  (AES‑256)        └────┬───────┘  (CID)       └────────────┘
                                       │
                                       │  Log (CID, meta)
                                       ▼
                              ┌────────────────────┐
                              │   SQL Database     │
                              │ (SQLite/Postgres)  │
                              └────────────────────┘
```

---

## 🧰 Tech Stack

| Layer         | Tech                        | Why                                                |
| ------------- | --------------------------- | -------------------------------------------------- |
| Backend API   | **Flask 2.x**               | Lightweight, Pythonic, great for rapid prototyping |
| Crypto        | **cryptography**            | Battle‑tested AES‑GCM implementation               |
| Storage       | **IPFS @ Pinata**           | Decentralised, CDN‑backed, pin‑guaranteed          |
| Audit Log     | **SQLite / PostgreSQL**     | Simple, reliable, ACID‑compliant                   |
| Frontend      | **HTML & Bootstrap 5**      | Simple, responsive                                 |
| DevOps (opt.) | **Docker + docker‑compose** | One‑command reproducible setup                     |

---

## 🔧 Prerequisites

* Python ≥ 3.11
* Git, make (optional but handy)
* Pinata account (JWT token)
* SQLite (bundled with Python) or PostgreSQL 14+

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
$ git clone https://github.com/<your‑user>/blockvault.git && cd blockvault

# 2. Create virtual environment
$ python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install Python deps
$ pip install -r requirements.txt

# 4. Copy env template & add secrets
$ cp .env.example .env
$ $EDITOR .env  # fill in PINATA_JWT, SECRET_KEY, DATABASE_URL

# 5. (Optional) Build Docker services
$ docker-compose up --build

# 6. Run the Flask API locally
$ python app.py  # visits http://127.0.0.1:5000
```

---

## 🔐 Configuration

All sensitive settings live in **`.env`** (never commit it!).

```dotenv
# Flask
SECRET_KEY="replace‑me‑with‑32‑random‑bytes"

# Pinata
PINATA_JWT="eyJhbGciOi..."

# Database
# For SQLite (default)
DATABASE_URL="sqlite:///blockvault.db"
# For Postgres (example)
# DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/blockvault"
```

---

## 🚀 Usage

### 1️⃣ Upload a File (Web UI)

1. Navigate to `http://localhost:5000`.
2. Choose any file ≤ 100 MB (configurable).
3. Click **Upload**.
4. The UI shows:

   * **CID** returned by Pinata.
   * **Local encryption key** *(displayed once — copy it!)*.
   * **Database record ID** for the audit log.

### 2️⃣ Retrieve & Decrypt via CLI

```bash
$ python scripts/download_and_decrypt.py QmCIDgoesHere --key <32‑byte‑hex>
```

---

## 🗃️ Database Schema

| Table   | Columns                                                     |
| ------- | ----------------------------------------------------------- |
| uploads | id (PK), cid, filename, mimetype, size\_bytes, uploaded\_at |

*`uploaded_at` is UTC; indexes on `cid` and `uploaded_at` for fast retrieval.*

---

## 🧪 Testing

```bash
# Python unit tests
$ pytest -v
```

---

## 🛣️ Roadmap

* [ ] **Role‑based access control** (JWT)
* [ ] **Key management** (HashiCorp Vault or AWS KMS)
* [ ] **Secure share links** with expiring tokens
* [ ] **Tamper‑evident DB hashing**
* [ ] **CI/CD** (GitHub Actions + Snyk)

Have a feature idea? [Open an issue](https://github.com/<your‑user>/blockvault/issues) or submit a PR.

---

## 🤝 Contributing

1. Fork 🍴 the repo.
2. Create a feature branch: `git checkout -b feat/amazing‑idea`.
3. Commit your changes with 🎯 clear messages.
4. `git push` and open a PR against **`dev`**.

> All contributions must pass `pre‑commit` hooks and unit tests. No red builds, no exceptions.

---

## ⚖️ License

`MIT` — do whatever you want, just don’t blame us when you accidentally upload your tax returns in plaintext. 😉

---

> **Maintainer:** shahiz  •  *Cybersecurity & DevSecOps tinkerer*

Happy vaulting! 📂🔐
