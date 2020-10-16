import requests
import hashlib
from sys import argv, exit


def call_api(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"There might be some error in the api call, please check it and try again\nError code: {res.status_code}, ")
    return res


def pawnage_counts(response_hashes, hash_to_check):
    hashes = (line.split(':') for line in response_hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0


def collect_api_response(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = call_api(first5_char)
    return pawnage_counts(response, tail)


def main(args):
    for password in args:
        count = collect_api_response(password)
        if count:
            print(
                f'{password} was found {count} times you must change your password.')
        else:
            print(f"{password} not found in the pawned database, you are safe.")


if __name__ == '__main__':
    if len(argv) > 1:
        try:
            exit(main(argv[1:]))
        except Exception as e:
            print(f"Ohh noo... Something went wrong...\nError details: {e}")
    else:
        print("Please provide valid arguments with the script.\nUsage: script.py arg1 arg2...")
