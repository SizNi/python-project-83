import requests


def req_url(url):
    try:
        response = requests.get(url)
        print(response.status_code)
        return response.status_code
    except Exception as exc:
        print(exc)
        return 'error'


if __name__ == '__main__':
    req_url()
