import urllib.parse as urlparse
import requests, optparse, re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-w", "--wordlist", dest="wordlist", help="Wordlist for searching")
    parser.add_option("-t", "--target_url", dest="target_url", help="Target Website")
    parser.add_option("-o", "--option", dest="option", help="Options such as s for subdomain, d for directory search, l for links in page and cl for finding main links in website")
    (options, arguments) = parser.parse_args()

    if not options.target_url:
        parser.error("Please input Target Website, use --help for more info.")
    elif not options.option:
        parser.error("Please input option, use --help for more info.")
    if options.option in ['s', 'd'] and not options.wordlist:
        parser.error("Please specify wordlist for this option, use --help for more info.")
    return options

options = get_arguments()
target_links = []
target_url = options.target_url

def request(url):
    try:
        if "http://" in url:
            return requests.get(url)
        elif "https://" in url:
            return requests.get(url)
        if requests.get("http://" + url) is None:
            return requests.get("https://" + url)
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

def find_subdomains(url, wordlist):
    url = url.replace("https://", "").replace("http://", "")

    with open(wordlist, "r") as wordlt:
        for line in wordlt:
            word = line.strip()
            test_url = word + "."+ url
            response = request(test_url)
            if response:
                print("[+] Discovered subdomains --> " + test_url)

def find_directories(url, wordlist):
    with open(wordlist, "r") as wordlt:
        for line in wordlt:
            word = line.strip()
            if target_url[-1] == '/':
                test_url = url + word
            else:
                test_url = url + "/" + word
            response = request(test_url)
            if response:
                print("[+] Discovered URL --> " + test_url)

def find_links(url):
    response = request(url)
    return re.findall(r'(?:href=")(.*?)"', response.content.decode(errors="ignore"))

def crawl(url):
    links = find_links(url)

    for link in links:
        link = urlparse.urljoin(url, link)
        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)

try:
    if options.option == 's':
        find_subdomains(options.target_url, options.wordlist)
    elif options.option == 'd':
        find_directories(options.target_url, options.wordlist)
    elif options.option == 'l':
        links = find_links(options.target_url)
        for link in links:
            link = urlparse.urljoin(options.target_url, link)
            print(link)
    elif options.option == 'cl':
        crawl(options.target_url)
    else:
        print("Please input correct option, use --help for more info.")

except KeyboardInterrupt:
    print("\nDetecting CTRL+C")
    print("Aborting....")

