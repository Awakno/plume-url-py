# Plume URL API

Plume URL API is an unofficial Python wrapper for the Plume URL shortening service.

## Installation

To install the library, use pip:

```sh
pip install PlumeURL
```

## Usage

Here's a basic example of how to use the library:

```python
import asyncio
from plumeurl import PlumeUrlAPI

api = PlumeUrlAPI("your_api_key_here")

async def main():
    # Create a new URL
    short_url = await api.create_url("https://www.google.com/")
    print(f"Short URL: {short_url}")

    # Search for a URL
    search_result = await api.search_url("custom_id")
    print(f"Search Result: {search_result}")

    # Get a URL
    url_info = await api.get_url("short_url_id")
    print(f"URL Info: {url_info}")

    # Edit a URL
    edited_url = await api.edit_url("short_url_id", "https://www.new-url.com/")
    print(f"Edited URL: {edited_url}")

    # Delete a URL
    delete_result = await api.delete_url("short_url_id")
    print(f"Delete Result: {delete_result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
