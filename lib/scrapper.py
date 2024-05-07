import requests
from bs4 import BeautifulSoup

class Scrapper:
    
    def __init__(self, value):
        self.value = value

    @staticmethod
    def handle_http_response(response):
        # Use map to handle and return common http/s codes instead of bunch of if else block.
        status_map = {
            200: "Success: Request was successful and content returned.",
            404: "Not Found: Server could not find the requested resource.",
            403: "Forbidden: Server is refusing to respond to the request.",
            401: "Unauthorized: Authentication is required for the request.",
            500: "Internal Server Error: Server-side error prevented fulfillment.",
            503: "Service Unavailable: Server is temporarily unable to handle the request.",
            429: "Too Many Requests: Sending too many requests in a given time frame.",
            301: "Moved Permanently: Requested resource has moved permanently.",
            302: "Found: Requested resource temporarily moved to a different URL.",
        }
        
        # When you get http 301 or 302, means the resource has moved to a new location. Try to find that new location.
        if response.status_code in [301, 302]:
            try:
                new_location = response.headers.get('Location')
                return f"{status_map.get(response.status_code, 'Unknown Status Code: Check documentation for details.')} New location: {new_location}"
            
            except Exception as e:
                return f"Error retrieving new location: {e}"
            
        else:
            return status_map.get(response.status_code, "Unknown Status Code: Check documentation for details.")

    @staticmethod
    def scrape_url(url):
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize a dictionary to store tags and their content
            tag_groups = {}

            # Find all tags in the HTML content
            all_tags = soup.find_all()

            # Group tags by their tag names
            for tag in all_tags:
                tag_name = tag.name # Get the tag name
                tag_content = tag.text.strip() if tag.text else "" # Get the tag's text content, if empty, output ""
                
                # If the tag exists in the dictionary, append new content under this tag, else insert a new tag with the category.
                if tag_name in tag_groups:
                    tag_groups[tag_name].append(tag_content)
                else:
                    tag_groups[tag_name] = [tag_content]
                    
            # Print the grouped tags and their content, if empty
            if tag_groups:
                for tag_name, tag_contents in tag_groups.items():
                    print(f"======= Tag: {tag_name} =======\n")
                    for content in tag_contents:
                        print(content)
                print("\n")
                    
            else:
                print("There are no content in the target URL.")
                
        else:
            print("Failed to fetch URL.", Scrapper.handle_http_response(response))
        