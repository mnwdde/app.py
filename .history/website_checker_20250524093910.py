import requests  # Import the requests library to make HTTP requests

def check_website(url):  # Define a function to check website status
    try:
        response = requests.get(url)  # Send GET request to the URL
        if response.status_code == 200:
            print(f"[+] {url} is UP! Status Code: {response.status_code}")
        else:
            print(f"[-] {url} returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error: Could not reach {url}")
        print("Details:", e)

def main():
    websites = [
        "https://www.saucekidsgang.com",
        
    ]

    for site in websites:  # Loop through list of websites
        check_website(site)  # Call function to check each site

if __name__ == "__main__":
    main()  # Run the main function
