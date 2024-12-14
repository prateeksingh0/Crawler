import urllib.parse as urlparse
import requests, optparse, re

target_links = []

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

def request(target_url):
    try:
        if "http://" in target_url:
            return requests.get(target_url)
        elif "https://" in target_url:
            return requests.get(target_url)
        if requests.get("http://" + target_url) is None:
            return requests.get("https://" + target_url)
        return requests.get("http://" + target_url)
    except requests.exceptions.ConnectionError:
        pass

def find_subdomains(target_url, wordlist):
    target_url = target_url.replace("https://", "").replace("http://", "")

    with open(wordlist, "r") as wordlt:
        for line in wordlt:
            word = line.strip()
            test_url = word + "."+ target_url
            response = request(test_url)
            if response:
                print("[+] Discovered subdomains --> " + test_url)

def find_directories(target_url, wordlist):
    with open(wordlist, "r") as wordlt:
        for line in wordlt:
            word = line.strip()
            if target_url[-1] == '/':
                test_url = target_url + word
            else:
                test_url = target_url + "/" + word
            response = request(test_url)
            if response:
                print("[+] Discovered URL --> " + test_url)

def find_links(target_url):
    response = request(target_url)
    return re.findall(r'(?:href=")(.*?)"', response.content.decode(errors="ignore"))

def crawl(target_url):
    links = find_links(target_url)

    for link in links:
        link = urlparse.urljoin(target_url, link)
        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


options = get_arguments()

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

