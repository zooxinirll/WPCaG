### WPCaG - WordPress Comprehensive Analyzer and Gatherer

WPCaG is a comprehensive tool designed for security researchers and WordPress administrators. It offers a wide range of features for gathering information, detecting vulnerabilities, and analyzing security configurations of WordPress websites.

## Main Menu Features :

• WordPress Version Detection: Identifies the installed WordPress version.

• Sitemap and robots.txt Fetcher: Retrieves sitemap.xml and robots.txt for further analysis.

• SSL Certificate Information: Gathers details about the SSL certificate, including issuer and expiration date.

• User Enumeration: Extracts WordPress user data from the REST API, if exposed.

• Plugins and Themes Detection: Detects common plugins and themes used by the WordPress site.

• Email Address Extraction: Extracts email addresses from the website content.

• Randomized User-Agent Requests: Bypasses basic security measures by randomizing request headers.

# Requirements

Python 3.6+ Required 

Python packages:requestsargparserichpyfiglethalo

## Installation

Clone the repository :

```bash
git clone https://github.com/zooxinirll/WPCaG.git
```

```bash
cd WPCaG
```
```bash
pip install -r requirements.txt
```


# Run
```
python3 WPCaG.py --single <URL>
```
# Single URL Analysis:
```
python3 WPCaG.py --single <URL> 
```
Analyzes a single WordPress site.

# Multiple URLs Analysis:
```
python3 WPCaG.py --multiple <URL1>,<URL2>,<URL3> 
```
Analyzes multiple WordPress sites separated by commas.

### 🌐 Connect With Me
<p align="center"> <a href="https://github.com/zooxinirll" target="_blank"> <img src="https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white" /> </a> <a href="https://www.instagram.com/h3r.10c4lh0st.07?igsh=MTRqcGNsdmN3a2FyaA==" target="_blank"> <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" /> </a></p>

### 🧠 Let's Collaborate
I'm always open to discussing new projects, innovative ideas, and opportunities. Feel free to reach out via my social platforms!
