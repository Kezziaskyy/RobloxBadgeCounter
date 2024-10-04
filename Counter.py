import requests
import time

# Function to count the number of badges a specific Roblox user has
def count_user_badges(user_id):
    # Base URL to get the badges of the user
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100"
    total_badges = 0
    retries = 5  # Number of retries if there's a connection issue

    # Loop through pages of badges until there are no more
    while url:
        for attempt in range(retries):
            try:
                # Send a GET request to fetch badge data
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors
                break  # Exit retry loop if request was successful
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                # Print a friendly retry message
                if attempt < retries - 1:
                    print(f"Connection error, retrying... ({attempt + 1}/{retries})")
                    time.sleep(2)  # Wait for a bit before retrying
                else:
                    # If max retries reached, print an error and exit
                    print("Max retries reached. Could not connect.")
                    return
            except requests.exceptions.RequestException as e:
                # Handle other types of errors
                print("An error occurred:", e)
                return

        # Parse the JSON response and count the badges
        data = response.json()
        total_badges += len(data['data'])

        # Check if there's another page of badges
        next_page = data.get('nextPageCursor')
        if next_page:
            # Update the URL to the next page
            url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&cursor={next_page}"
        else:
            # No more pages to process
            url = None

    return total_badges

# Main part of the script
if __name__ == "__main__":
    user_id =   # Replace with your Roblox user ID
    badge_count = count_user_badges(user_id)

    # Print the result
    if badge_count is not None:
        print(f"User ID {user_id} has {badge_count} badges.")
