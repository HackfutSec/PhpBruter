Here's a comprehensive README.md file for your GitHub repository:

```markdown
# PhpBruter - phpMyAdmin Enterprise Pentesting Tool

![Banner](https://freeimage.host/i/FTnzmqg)

**PhpBruter** is an advanced security testing tool designed for professional penetration testers to assess the security of phpMyAdmin installations. This enterprise-grade tool provides multiple attack vectors to test authentication security with features like credential brute-forcing, password spraying, and custom wordlist attacks.

## Features

- 🚀 **Multi-mode operation** (Default scan, Wordlist attack, Single test, Password spray)
- 🔒 **Thread-safe operations** with configurable thread limits
- 📊 **Results persistence** (Automatically saves found credentials to JSON)
- 🌐 **Proxy support** for routing traffic through intermediaries
- 🕵️ **IP rotation** with random X-Forwarded-For headers
- ⏱️ **Performance metrics** with response time tracking
- 🎨 **Color-coded output** for easy result interpretation
- 📁 **Wordlist validation** with proper error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HackfutSec/PhpBruter.git
cd PhpBruter
```

2. Install dependencies:
```bash
pip install requests colorama
```

## Usage

Basic usage:
```bash
python3 phpmyadmin_pentest.py [target_url]
```

Or run without arguments for interactive mode:
```bash
python3 phpmyadmin_pentest.py
```

### Modes Available:
1. **Default Credential Scan** - Tests common phpMyAdmin credentials
2. **Custom Wordlist Attack** - Uses provided username and password wordlists
3. **Single Credential Test** - Tests one specific username/password combination
4. **Password Spray Attack** - Tests one username against a password wordlist

## Configuration

Edit the `CONFIG` dictionary in the script to customize:
```python
CONFIG = {
    "user_agents": [...],  # Customize user agents
    "default_users": [...],  # Add default usernames
    "default_passwords": [...],  # Add default passwords
    "timeout": 15,  # Request timeout
    "delay": 1.5,  # Delay between attempts
    "max_threads": 5,  # Maximum concurrent threads
    "results_file": "scan_results.json",  # Output file
    "proxy": None  # Configure proxies if needed
}
```

## Sample Wordlists

Example wordlists are provided in the `wordlists/` directory:
- `common_users.txt` - Common phpMyAdmin usernames
- `common_passwords.txt` - Common phpMyAdmin passwords

## Legal Disclaimer

⚠️ **This tool is for authorized security testing and educational purposes only.**  
The developers assume no liability and are not responsible for any misuse or damage caused by this program. Only use on systems you own or have permission to test.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Screenshot

![Sample Usage](https://freeimage.host/i/screenshot-2025-06-24-1.FTnzmqg)
