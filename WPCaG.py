import requests
import random
import argparse
import socket
import ssl
import re
from urllib.parse import urlparse
from halo import Halo
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# List of User-Agents to randomize requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
]

# Display Figlet Banner
def display_banner():
    fig = pyfiglet.Figlet(font='standard')
    banner = fig.renderText("WPCaG")
    console.print(banner, style="bold magenta")
    console.print("Author: LocalHost.07", style="green")

# Fetch WordPress version
def fetch_wp_version(base_url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    possible_endpoints = ['', 'wp-links-opml.php', 'readme.html']

    for endpoint in possible_endpoints:
        url = normalize_url(base_url, endpoint)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            if 'generator' in response.text:
                start = response.text.find('generator') + len('generator') + 9
                end = response.text.find('"', start)
                generator_content = response.text[start:end]
                if 'WordPress' in generator_content:
                    version = generator_content.split('WordPress ')[-1]
                    return version

            if 'WordPress' in response.text:
                version_index = response.text.lower().find("wordpress")
                if version_index != -1:
                    version_start = version_index + len("wordpress ")
                    version_end = response.text.find("<", version_start)
                    return response.text[version_start:version_end].strip()

        except requests.RequestException:
            continue

    return "Unknown"

# Fetch Sitemap
def fetch_sitemap(base_url):
    url = normalize_url(base_url, 'sitemap.xml')
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return url
        return "Sitemap not found"
    except requests.RequestException:
        return "Sitemap not found"

# Fetch robots.txt
def fetch_robots_txt(base_url):
    url = normalize_url(base_url, 'robots.txt')
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return url
        return "robots.txt not found"
    except requests.RequestException:
        return "robots.txt not found"

# Fetch SSL Certificate Information
def get_ssl_info(url):
    hostname = url.split("//")[-1].split("/")[0]
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                console.print(f"Issuer: {issuer['organizationName']}, Expiration Date: {cert['notAfter']}")
    except Exception as e:
        console.print(f"Failed to get SSL info for {url}: {str(e)}")

# Fetch WordPress Users via REST API
def fetch_user_data(base_url):
    url = normalize_url(base_url, 'wp-json/wp/v2/users')
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        users = response.json()
        if not isinstance(users, list) or not users:
            return None
        return [{
            "Username": user.get("name", "N/A"),
            "Role": ', '.join(user.get("roles", ["N/A"])),
            "Email": user.get("email", "N/A"),
            "First Name": user.get("first_name", "N/A"),
            "Last Name": user.get("last_name", "N/A"),
            "Website": user.get("url", "N/A"),
            "Bio": user.get("description", "N/A")
        } for user in users]
    except requests.RequestException:
        return None

# Fetch Plugins and Themes Data
def fetch_plugins_themes(base_url):
    plugins = []
    themes = []
    headers = {'User-Agent': random.choice(USER_AGENTS)}

    # Detect common plugins
    common_plugins = ['akismet', 'contact-form-7', 'wordpress-seo', 'jetpack', 'elementor', 'woocommerce', 'wpforms-lite']
    for plugin in common_plugins:
        plugin_url = normalize_url(base_url, f'/wp-content/plugins/{plugin}/readme.txt')
        try:
            response = requests.get(plugin_url, headers=headers, timeout=5)
            if response.status_code == 200:
                plugins.append(plugin)
        except requests.RequestException:
            continue

    # Detect common themes
    common_themes = ['twentytwentyone', 'twentytwentytwo', 'astra', 'hello-elementor', 'generatepress', 'oceanwp', 'neve']
    for theme in common_themes:
        theme_url = normalize_url(base_url, f'/wp-content/themes/{theme}/style.css')
        try:
            response = requests.get(theme_url, headers=headers, timeout=5)
            if response.status_code == 200:
                themes.append(theme)
        except requests.RequestException:
            continue

    return {
        "Plugins": plugins if plugins else ["Not Detected"],
        "Themes": themes if themes else ["Not Detected"]
    }

# Extract email addresses using regex
def extract_emails(page_content):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, page_content)

# Display user data
def display_user_data(user_data):
    if user_data:
        console.print("[bold cyan]User Data:[/bold cyan]")
        for user in user_data:
            console.print(Panel(f"[bold]Username:[/bold] {user['Username']}\n"
                                f"[bold]Role:[/bold] {user['Role']}\n"
                                f"[bold]Email:[/bold] {user['Email']}\n"
                                f"[bold]First Name:[/bold] {user['First Name']}\n"
                                f"[bold]Last Name:[/bold] {user['Last Name']}\n"
                                f"[bold]Website:[/bold] {user['Website']}\n"
                                f"[bold]Bio:[/bold] {user['Bio']}", title=f"User Info", border_style="green"))
    else:
        console.print("[yellow]No user data found.[/yellow]")

# Display plugins and themes data
def display_plugins_themes(plugins_themes):
    plugins = plugins_themes['Plugins']
    themes = plugins_themes['Themes']

    plugins_table = Table(title="Detected Plugins")
    plugins_table.add_column("Plugins", justify="center", style="cyan", no_wrap=True)

    for plugin in plugins:
        plugins_table.add_row(plugin)

    themes_table = Table(title="Detected Themes")
    themes_table.add_column("Themes", justify="center", style="magenta", no_wrap=True)

    for theme in themes:
        themes_table.add_row(theme)

    console.print(plugins_table)
    console.print(themes_table)

# Display extracted email addresses
def display_extracted_emails(emails):
    if emails:
        email_table = Table(title="Extracted Email Addresses", show_header=True, header_style="bold cyan")
        email_table.add_column("Emails", justify="center", style="bold yellow")

        for email in emails:
            email_table.add_row(email)

        console.print(email_table)
    else:
        console.print("[yellow]No email addresses found.[/yellow]")

# Initialize spinner and fetch data
def run_analysis(base_url):
    spinner = Halo(text='Fetching WordPress Version...', spinner='dots')
    spinner.start()
    version = fetch_wp_version(base_url)
    spinner.succeed(f"WordPress Version: {version}")

    spinner.text = 'Fetching Sitemap...'
    spinner.start()
    sitemap = fetch_sitemap(base_url)
    spinner.succeed(sitemap)

    spinner.text = 'Fetching Robots.txt...'
    spinner.start()
    robots_txt = fetch_robots_txt(base_url)
    spinner.succeed(robots_txt)
    
    spinner.text = 'Fetching SSL Information...'
    spinner.start()
    get_ssl_info(base_url)
    spinner.succeed("SSL Information Fetched.")

    spinner.text = 'Fetching User Data...'
    spinner.start()
    user_data = fetch_user_data(base_url)
    spinner.succeed("User Data Fetched.")
    display_user_data(user_data)

    spinner.text = 'Fetching Plugins and Themes Data...'
    spinner.start()
    plugins_themes = fetch_plugins_themes(base_url)
    spinner.succeed("Plugins and Themes Data Fetched.")
    display_plugins_themes(plugins_themes)

    spinner.text = 'Extracting Email Addresses...'
    spinner.start()
    try:
        response = requests.get(base_url, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=10)
        emails = extract_emails(response.text)
        spinner.succeed("Email Addresses Extracted.")
        display_extracted_emails(emails)
    except requests.RequestException:
        spinner.fail("Failed to extract emails.")

# Normalize URL function to ensure URL formatting
def normalize_url(base_url, endpoint):
    if not base_url.endswith('/'):
        base_url += '/'
    return base_url + endpoint

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="WP-CaG - WordPress Comprehensive Analyzer and Gatherer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--single', type=str, help='Single URL to analyze')
    group.add_argument('--multiple', type=str, help='Multiple URLs to analyze, separated by commas')
    return parser.parse_args()

# Validate and prepare the URL
def validate_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'http://' + url
    return url

# Main function to execute the tool
def main():
    display_banner()
    
    args = parse_arguments()

    if args.single:
        base_url = validate_url(args.single)
        run_analysis(base_url)

    elif args.multiple:
        urls = args.multiple.split(',')
        for url in urls:
            base_url = validate_url(url.strip())
            console.print(f"[bold green]Analyzing {base_url}[/bold green]")
            run_analysis(base_url)
            console.print("[bold blue]Analysis Completed for this URL[/bold blue]\n")

if __name__ == '__main__':
    main()
