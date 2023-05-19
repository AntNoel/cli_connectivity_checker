from http.client import HTTPConnection,HTTPSConnection
from urllib.parse import urlparse
import asyncio, aiohttp

def site_is_online(url, timeout=2):
    """Return True if the target url is online Raise an exception otherwise."""

    error = Exception('unknown error')
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]

    for port in (80, 443):
        conn = HTTPConnection(host=host, port=port, timeout=timeout )
        try:
            conn.request('HEAD', '/')
            return True
        except Exception as e:
            error = e
        finally:
            conn.close()
    raise error

async def site_is_online_async(url, timeout=2):
    """zReturn true if the target url is online raise an exception otherwise."""
    error = Exception('unknown error')
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]

    for scheme in ("http", "https"):
        target_url = f"{scheme}://{host}"
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            
            except asyncio.exceptions.TimeoutError:
                error = Exception("timed out")
            except Exception as e:
                error = e
    raise error


#Perform single http get request

def get_request(url):
    if not url:
        return
    
    conn = HTTPConnection(url)

    try:
        conn.request('HEAD', '/')
    except ConnectionError:
        return 'offline'
    
    return 'online'



