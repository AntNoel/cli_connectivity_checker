import argparse

def read_user_cli_args():
    """Handle the cli arguments and options"""

    parser = argparse.ArgumentParser(
        prog='rpchecker', 
        description="Check the availability of websites"
    )
    parser.add_argument(
        '-u', 
        '--urls',
        metavar='URLs',
        nargs='+',
        type=str,
        default=[],
        help="Enter one or more website URLS"
    )
    
    parser.add_argument(
        '-f',
        '--input-files',
        metavar='FILE',
        type=str,
        default='',
        help="Read URLs from a file"
    )

    parser.add_argument(
        "-a", 
        "--asynchronous", 
        action="store_true", 
        help="run the connectivity check asynchronously",
    )
    
    return parser.parse_args() #returns namespace object with the args



def display_check_result(result, url, response_time,error=""):
    """Display the result of a connectivity check"""
    print(f'The status of "{url} is: ', end="")
    if result:
        print("Online 👍")
        print(response_time)
    else:
        print(f"Offline 👎 \n  Error: {error}")
        print(response_time)


        