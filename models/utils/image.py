"""Image processing module."""

from urllib import request


def download_image(image_url, save_path):
    """Function to download image form URL."""

    try:
        request.urlretrieve(image_url, save_path)
        return True
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False
