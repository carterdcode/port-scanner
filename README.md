# 🔍 Python Port Scanner

## ⚠️ Disclaimer

This tool is intended **for educational and authorized security testing purposes only**.

- **Do not** use this tool against networks, systems, or devices you do not own or do not have explicit permission to test.
- Unauthorized scanning may be illegal and could result in criminal charges.
- By using this tool, you agree that the author(s) are **not responsible** for any misuse or damages caused.

Use responsibly.

---

## 🛠 Usage

### ▶️ Run from the command line

1. Navigate to the `src/` directory:
   ```bash
   cd src
   ```

2. Run the scanner:
   ```bash
   python port-scanner.py <host> [-p <port-range>] [-n <num-threads>]
   ```

#### 🔹 Example:
```bash
python port-scanner.py 192.168.0.1 -p 1-5000 -n 100
```

- `-p`: Port range (default is `1-1024`)
- `-n`: Number of threads (default is `10`)

You can omit `-p` and `-n` to use the default values.

---

## 🐳 Run with Docker

1. Navigate to the `port-scanner/src` directory:
   ```bash
   cd port-scanner/src
   ```

2. Build the Docker image:
   ```bash
   docker build -t port-scanner .
   ```

3. Run the scanner using Docker:
   ```bash
   docker run --rm -it port-scanner <host> -p <port-range> -n <num-threads>
   ```

#### 🔹 Example:
```bash
docker run --rm -it port-scanner 192.168.0.1 -p 1-5000 -n 100
```

---

## 📂 Directory Structure

```
port-scanner/
├── .devcontainer/
│   ├── devcontainer.json
│   └── banner.sh
├── src/
│   ├── port-scanner.py
│   └── ...
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ✅ Tip

If you're using GitHub Codespaces, the terminal will automatically start in the `src/` directory and display usage instructions.

---
