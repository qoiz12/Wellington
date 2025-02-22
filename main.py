from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import zipfile
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import json
from datetime import datetime, timedelta
from flask_cors import CORS  # Import CORS for cross-origin requests

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Authentication setup
auth = HTTPBasicAuth()

# Secure username and password (store these securely, e.g., in environment variables)
USERNAME = "USER"
PASSWORD_HASH = generate_password_hash("PASS")  # Hash the password

# Verify password
@auth.verify_password
def verify_password(username, password):
    if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
        return username

# Global variables
EXTRACT_DIR = "extracted_domains"
output_json = "scam_popups_results.json"
SCREENSHOT_DIR = "screenshots"
scams_txt = "scams.txt"

# Credit
print("Created by Qoiz12, Hosted on Netcup.")

# URL to the page containing newly registered domains
DOMAINS_URL = "https://shreshtait.com/newly-registered-domains/nrd-1w"

# Timeout for requests (in seconds)
REQUEST_TIMEOUT = 45

# File to store scanned domains and their timestamps
SCANNED_DOMAINS_FILE = "scanned_domains.json"

# Function to load scanned domains from the JSON file
def load_scanned_domains():
    if os.path.exists(SCANNED_DOMAINS_FILE):
        with open(SCANNED_DOMAINS_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save scanned domains to the JSON file
def save_scanned_domains(scanned_domains):
    with open(SCANNED_DOMAINS_FILE, "w") as file:
        json.dump(scanned_domains, file, indent=4)

# Function to check if a domain should be scanned
def should_scan_domain(domain, scanned_domains):
    if domain in scanned_domains:
        last_scanned = datetime.fromisoformat(scanned_domains[domain])
        # Rescan if it's been more than 1 week since the last scan
        return datetime.now() - last_scanned > timedelta(weeks=1)
    return True

# Function to update the scanned domains with the current timestamp
def update_scanned_domains(domain, scanned_domains):
    scanned_domains[domain] = datetime.now().isoformat()
    save_scanned_domains(scanned_domains)

# Function to read domains from the webpage
def read_domains_from_webpage(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        domains = [line.strip() for line in soup.get_text().splitlines() if line.strip()]
        return domains
    except Exception as e:
        print(f"Error reading domains from {url}: {e}")
        return []

# Function to check if a domain is redirected or parked
def is_redirected_or_parked(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
        if response.history:
            print(f"{url} is a redirect.")
            return True
        soup = BeautifulSoup(response.text, 'html.parser')

        # Common indicators of parked domains
        parked_keywords = [
            "this domain is parked", "domain for sale", "parked domain",
            "this domain is available", "buy this domain", "Parked at", "is already taken", "domain parking"
        ]

        # Check for parked domain keywords in the page content
        if any(keyword in response.text.lower() for keyword in parked_keywords):
            print(f"{url} is a parked domain.")
            return True

        # Check for common parked domain services
        parked_services = ["sedoparking.com", "godaddy.com", "parkingcrew.net", "loopia.se", "nazwa.pl", "site.eu", "svenskadomaner.se", "serverpoint.com", "riktad.com", "abansys.com", "networksolutions.com", "abion.com", "above.com", "domain.cam", "namebright.com", "regne.net", "acens.com", "dnspod.com", "networksolutions.com", "namebright.com", "networksolutions.com", "active.domains", "networksolutions.com", "addresscreation.com", "addressontheweb.com", "networksolutions.com", "networksolutions.com", "ait.com", "networksolutions.com", "turhost.com/domain", "afproxy.africa", "afriregister.com", "networksolutions.com", "akky.mx", "alantron.com", "networksolutions.com", "networksolutions.com", "alfena.com", "net.cn", "wanwang.aliyun.com", "alibabacloud.com", "networksolutions.com", "allaccessdomains.com", "alldomains.com", "networksolutions.com", "networksolutions.com", "networksolutions.com", "alpinedomains.com", "domains.amazon", "registrar.amazon.com", "networksolutions.com", "networksolutions.com", "annulet.com", "anytimesites.com", "vebonix.com", "maprilis.net", "networksolutions.com", "networksolutions.com", "networksolutions.com", "heberjahiz.com", "arsys.es", "aruba.it", "ascio.com", "networksolutions.com", "atakdomain.com", "ati.tn", "networksolutions.com", "networksolutions.com", "networksolutions.com", "networksolutions.com", "austriadomains.com", "austriandomains.com", "authenticweb.com", "wordpress.com", "namebright.com", "azdomainz.com", "azprivatez.com"
        ]
        if any(service in response.text.lower() for service in parked_services):
            print(f"{url} is a parked domain.")
            return True

        return False
    except requests.exceptions.Timeout:
        print(f"{url} took too long to load (>{REQUEST_TIMEOUT} seconds). Skipping.")
        return True  # Treat timeout as a parked/redirected domain to skip it
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

# Function to check if a website is an adult or gambling site
def is_adult_or_gambling_site(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Keywords for adult websites (Chinese Only)
        adult_keywords = ["成人", "色情", "成人视频", "成人内容"]

        # Keywords for gambling websites (Chinese and English)
        gambling_keywords = [
            "赌场", "赌博", "彩票", "casino", "bet", "poker", "gambling", "slot"
        ]

        # Check for adult or gambling keywords in the page content
        if any(keyword in response.text.lower() for keyword in adult_keywords):
            print(f"{url} is an adult website. Skipping.")
            return True
        if any(keyword in response.text.lower() for keyword in gambling_keywords):
            print(f"{url} is a gambling website. Skipping.")
            return True

        return False
    except requests.exceptions.Timeout:
        print(f"{url} took too long to load (>{REQUEST_TIMEOUT} seconds). Skipping.")
        return True
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

# Function to scrape common elements from scam pop-ups
def scrape_scam_popups(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        common_elements = {
            "fake_security_alerts": [],
            "fake_progress_bars": [],
            "fake_buttons": [],
            "fullscreen_scripts": [],
            "audio_alerts": [],
            "fake_cursors": [],
            "fake_branding": [],
        }

        # Check for fake security alerts
        fake_alerts = soup.find_all(
            string=lambda text: text and "infected" in text.lower())
        common_elements["fake_security_alerts"] = [
            alert.strip() for alert in fake_alerts
        ]

        # Check for fake progress bars
        fake_progress_bars = soup.find_all(
            class_=lambda cls: cls and "progress" in cls.lower())
        common_elements["fake_progress_bars"] = [
            bar.get('class') for bar in fake_progress_bars
        ]

        # Check for fake buttons
        fake_buttons = soup.find_all(
            'button', string=lambda text: text and "cancel" in text.lower())
        common_elements["fake_buttons"] = [
            button.text.strip() for button in fake_buttons
        ]

        # Check for fullscreen scripts
        fullscreen_scripts = soup.find_all(
            'script',
            string=lambda text: text and "fullscreen" in text.lower())
        common_elements["fullscreen_scripts"] = [
            script.text.strip() for script in fullscreen_scripts
        ]

        # Check for audio alerts
        audio_alerts = soup.find_all('audio')
        common_elements["audio_alerts"] = [
            audio.get('src') for audio in audio_alerts
        ]

        # Check for fake cursors
        fake_cursors = soup.find_all(
            style=lambda style: style and "cursor: none" in style.lower())
        common_elements["fake_cursors"] = [
            cursor.get('style') for cursor in fake_cursors
        ]

        # Check for fake branding
        fake_branding = soup.find_all(string=lambda text: text and (
            "microsoft" in text.lower() or "google" in text.lower()))
        common_elements["fake_branding"] = [
            branding.strip() for branding in fake_branding
        ]

        return common_elements
    except requests.exceptions.Timeout:
        print(f"{url} took too long to load (>{REQUEST_TIMEOUT} seconds). Skipping.")
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to take a screenshot of the webpage
def take_screenshot(url, screenshot_dir):
    try:
        # Create the screenshots directory if it doesn't exist
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # Generate a filename based on the domain
        domain = url.split("//")[1].replace("/", "_")
        screenshot_path = os.path.join(screenshot_dir, f"{domain}.png")

        # Set up Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Install ChromeDriver and Chrome
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(2)  # Wait for the page to load
        driver.save_screenshot(screenshot_path)
        driver.quit()
        print(f"Screenshot saved to {screenshot_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")

# Function to categorize scams as "potential" or "very likely"
def categorize_scam(common_elements):
    if common_elements["fake_security_alerts"]:
        return "very likely"
    return "potential"

# Function to log scams to scams.txt
def log_scam(url, category, phone_numbers):
    with open("scams.txt", "a") as file:
        file.write(f"Scam found: {url}\n")
        file.write(f"Category: {category}\n")
        if phone_numbers:
            file.write(f"Phone numbers: {', '.join(phone_numbers)}\n")
        file.write("\n")

# Main function to scrape multiple URLs and save results
def main(DOMAINS_URL, extract_dir, output_json, screenshot_dir, scams_txt):
    results = []
    scanned_domains = load_scanned_domains()

    while True:
        # Continue with other domains
        domains = read_domains_from_webpage(DOMAINS_URL)

        for domain in domains:
            url = f"http://{domain}"
            if not should_scan_domain(domain, scanned_domains):
                print(f"Skipping {url} (already scanned within the last week).")
                continue

            print(f"Scraping {url}...")
            if is_redirected_or_parked(url):
                print(f"{url} is not a scam.")
            elif is_adult_or_gambling_site(url):
                print(f"{url} is an adult or gambling site. Skipping.")
            else:
                common_elements = scrape_scam_popups(url)
                if common_elements and any(common_elements.values()):
                    print("Scam found!")
                    category = categorize_scam(common_elements)
                    phone_numbers = common_elements.get("fake_contact_numbers", [])
                    take_screenshot(url, screenshot_dir)
                    log_scam(url, category, phone_numbers)
                else:
                    print(f"No scam elements found in {url}, data discarded.")

            # Update the scanned domains list
            update_scanned_domains(domain, scanned_domains)

        print(f"Results saved to {scams_txt}")

        # Calculate time until next scan
        now = time.time()
        target_time = now - (now % 86400) + 7.5 * 3600  # Next 07:30 GMT
        if target_time < now:
            target_time += 86400  # Add 1 day if we've passed 07:30 today
            
        wait_seconds = target_time - now
        
        # Convert to human-readable format
        hours, rem = divmod(int(wait_seconds), 3600)
        minutes, seconds = divmod(rem, 60)
        time_parts = []
        if hours > 0:
            time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds > 0 or (hours == 0 and minutes == 0):
            time_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        
        print(f"\nNext scan scheduled at 07:30 GMT ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(target_time))})")
        print(f"Time until next scan: {', '.join(time_parts)}\n")
        
        time.sleep(wait_seconds)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control-panel')
@auth.login_required
def control_panel():
    return render_template('control-panel.html')

@app.route('/run_command', methods=['POST'])
@auth.login_required
def run_command():
    command = request.json.get('command')
    if command == 'scan':
        thread = threading.Thread(target=main, args=(DOMAINS_URL, EXTRACT_DIR, output_json, SCREENSHOT_DIR, scams_txt))
        thread.start()
        return jsonify({"message": "Scan started!"})
    return jsonify({"error": "Unknown command"}), 400

# Serve static files from the /templates/ folder
@app.route('/templates/<path:filename>')
def serve_template_file(filename):
    return send_from_directory('templates', filename)

# Serve static files from the EXTRACT_DIR
@app.route('/files/<path:filename>')
@auth.login_required
def serve_file(filename):
    return send_from_directory(EXTRACT_DIR, filename)

# Robots.txt route
@app.route('/robots.txt')
def robots_txt():
    response = Response("User-agent: *\nDisallow: /")
    response.headers["Content-Type"] = "text/plain"
    return response

# Example usage
if __name__ == "__main__":
    ZIP_URL = "https://whoisds.com//whois-database/newly-registered-domains/MjAyNS0wMS0yNi56aXA=/nrd"
    ZIP_FILE = "newly_registered_domains.zip"
    EXTRACT_DIR = "extracted_domains"
    output_json = "scam_popups_results.json"
    SCREENSHOT_DIR = "screenshots"
    scams_txt = "scams.txt"

    # Run the Flask app
    app.run(host='0.0.0.0', port=6945, debug=True)