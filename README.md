WPCaG - WordPress Comprehensive Analyzer and Gatherer�WPCaG is a comprehensive tool designed for security researchers and WordPress administrators. It offers a wide range of features for gathering information, detecting vulnerabilities, and analyzing security configurations of WordPress websites.FeaturesWordPress Version Detection: Identifies the installed WordPress version.Sitemap and robots.txt Fetcher: Retrieves sitemap.xml and robots.txt for further analysis.SSL Certificate Information: Gathers details about the SSL certificate, including issuer and expiration date.User Enumeration: Extracts WordPress user data from the REST API, if exposed.Plugins and Themes Detection: Detects common plugins and themes used by the WordPress site.Email Address Extraction: Extracts email addresses from the website content.Randomized User-Agent Requests: Bypasses basic security measures by randomizing request headers.RequirementsPython 3.6+Required Python packages:requestsargparserichpyfiglethaloInstallationClone the repository:git clone https://github.com/yourusername/WPCaG.gitNavigate to the directory:cd WPCaGInstall the required packages:pip install -r requirements.txtUsageRun the main script to access the tool's functionalities:python3 WPCaG.py --single <URL>Command-Line OptionsSingle URL Analysis:python3 WPCaG.py --single <URL>Analyzes a single WordPress site.Multiple URLs Analysis:python3 WPCaG.py --multiple <URL1>,<URL2>,<URL3>Analyzes multiple WordPress sites separated by commas.Main Menu FeaturesFetch WordPress Version: Identifies the installed WordPress version.Fetch Sitemap and robots.txt: Retrieves the sitemap.xml and robots.txt files for analysis.Fetch SSL Certificate Information: Displays the SSL certificate details.Enumerate Users: Extracts user data via the WordPress REST API.Detect Plugins and Themes: Identifies common plugins and themes installed on the WordPress site.Extract Email Addresses: Extracts email addresses found on the website.Exit: Exits the tool.🌐 Connect With Me�🧠 Let's CollaborateI'm always open to discussing new projects, innovative ideas, and collaboration opportunities. Feel free to reach out via my social platforms!