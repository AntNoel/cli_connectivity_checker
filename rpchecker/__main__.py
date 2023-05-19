import sys
import asyncio, time
from pathlib import Path
from rpchecker.cli import read_user_cli_args, display_check_result
from rpchecker.checker import site_is_online, site_is_online_async

def main():
    """Run RP Checker"""
    # Get the user args
    user_args = read_user_cli_args()
    # Get the websites urls
    urls = _get_websites_urls(user_args)
    #Check the urls for site online
    if not urls:
        print("Error: no URLs to check")
        sys.exit(1)
    
    if user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)


def _get_websites_urls(user_args):

    urls = user_args.urls
    if user_args.input_files:
        urls+= _read_urls_from_file(user_args.input_files)
    
    if not urls:
        print("Error: No urls provided")
        sys.exit(1)

    return urls


def _read_urls_from_file(input_file):
    
    file_path = Path(input_file)
    if file_path.is_file():
         with open(input_file, 'r') as file:
            final_urls = [url.strip() for url in file ]
            

    if not final_urls:
        print("No urls in that file")
        sys.exit()
   
    return final_urls

def _synchronous_check(urls):
    timer = Timer(text="Response time: {:.1f}")

    for url in urls:
        error = ""
        try:
            timer.start()
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        finally:
            response_time = timer.stop()
        display_check_result(result, url,response_time,error)

async def _asynchronous_check(urls):
    async def _check(url):
        error = ""
        try:
            result = await site_is_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

    await asyncio.gather(*(_check(url) for url in urls))
  


class TimerError(Exception):

    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self, text="The response time was {:0.4f} seconds"):
        self._start_time = None
        self.text = text

     
    def get_response_statement(self, elapsed_time):
        return self.text.format(elapsed_time)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop()  to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop an existing timer"""
        if self._start_time is None:
            raise TimerError("Timer isn't running. Use .start() to start timer"
                             )
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return self.get_response_statement(elapsed_time)
   


if __name__== "__main__":
    main()