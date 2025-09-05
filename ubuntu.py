import requests
import os
from urllib.parse import urlparse

def make_unique_filename(folder, filename):
    """Avoid overwriting duplicate files by adding _1, _2, etc."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

def main():
    print("🐧 Welcome to the Ubuntu Image Fetcher 🐧")
    print("A mindful tool for collecting images from the web\n")
    
    # Get multiple URLs from user (separated by spaces)
    urls = input("Enter one or more image URLs (separated by spaces): ").split()
    
    # Create folder if it doesn’t exist
    folder = "Fetched_Images"
    os.makedirs(folder, exist_ok=True)

    for url in urls:
        try:
            print(f"\n⬇️ Fetching {url} ...")

            # Fetch the image
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Precaution 1: Check Content-Type (only allow images)
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped: Not an image (Content-Type: {content_type})")
                continue

            # Precaution 2: Check Content-Length (skip if too big > 5MB)
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > 5 * 1024 * 1024:
                print(f"✗ Skipped: File too large ({int(content_length)/1024/1024:.2f} MB)")
                continue

            # Extract filename or use fallback
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or "downloaded_image.jpg"

            # Avoid duplicates
            filename = make_unique_filename(folder, filename)

            # Save the image
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):  # Save in chunks
                    f.write(chunk)

            print(f"✅ Saved: {filepath}")
            print("✓ Connection strengthened. Community enriched.")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
        except Exception as e:
            print(f"✗ An error occurred: {e}")

if __name__ == "__main__":
    main()
