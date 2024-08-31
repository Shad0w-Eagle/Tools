# Open Bug Bounty Finder CLI

## Overview

The **Open Bug Bounty Finder CLI** is a command-line tool for checking vulnerabilities on Open Bug Bounty. It allows you to input domains, check their vulnerability status, and save the results to a file. The tool also provides an option to automatically open the URLs in a web browser.

## Features

- Check multiple domains for vulnerabilities.
- Save the results to a file with separate sections for unpatched and patched URLs.
- Option to automatically open URLs in a web browser.

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library

## Installation

1. Ensure you have Python 3.x installed.
2. Install the required Python libraries by running:

   ```bash
   pip install requests tqdm

Usage
Command Line Arguments
-d, --domain-file (optional): Path to a file containing a list of domains to check (one domain per line).
-D, --domain (optional): A single domain to check.
-o, --output-file (required): Path to the file where results will be saved.
--open-browser (optional): Automatically open URLs in the browser without asking.

Examples
# Check a list of domains from a file and save results:
python3 script.py -d domains.txt -o results.txt

# Check a single domain and save results:
python3 script.py -D example.com -o results.txt

# Check domains and open URLs in the browser:
python3 script.py -d domains.txt -o results.txt --open-browser

# How It Works

Input Domains:
Provide either a file with a list of domains or a single domain.

Check Vulnerabilities:
For each domain, a search URL is constructed and queried to check for vulnerabilities.

Save Results:
Results are categorized into unpatched and patched URLs and saved to the specified file.

Open in Browser:
If the --open-browser flag is set or confirmed via prompt, URLs are opened in the default web browser.