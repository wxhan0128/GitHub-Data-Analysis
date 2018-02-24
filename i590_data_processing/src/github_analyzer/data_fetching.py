import requests
import json
from urllib.parse import urljoin
import getpass
import win_unicode_console


class DataFetching:
    def __init__(self, username, password):
        self.GITHUB_API = 'https://api.github.com'  # basic api address

        # username and password are for basic authorization
        self.username = username
        self.password = password

    def generate_authorization(self, auth_name):
        note = auth_name
        #
        # Compose Request
        #
        url = urljoin(self.GITHUB_API, 'authorizations')
        payload = {}
        if note:
            payload['note'] = note
        response = requests.post(
            url,
            auth=(self.username, self.password),
            data=json.dumps(payload),
        )

        if response.ok:
            # parse the request to json format, could also use res.json()
            auth_data = json.loads(response.text or response.content)
            # write the token to a local file since we cannot read token from get method
            file = open('token_file.txt', 'w')
            file.write('id %s' % auth_data['id'])
            file.write('token %s' % auth_data['token'])
        # if does not make any change, we cannot generate authorization repeatedly, it will return error
        else:
            print(json.dumps(response.json()['message'], indent=4))

    def get_authorization(self, auth_id):
        # combine the url
        url = urljoin(self.GITHUB_API, 'authorizations/' + auth_id)
        response = requests.get(
            url,
            auth=(self.username, self.password)
        )

        if response.ok:
            auth_data = json.loads(response.text or response.content)
            print(json.dumps(auth_data, indent=4))
        else:
            print(json.dumps(response.json()['message'], indent=4))

    def list_all_authorization(self):
        url = urljoin(self.GITHUB_API, 'authorizations')
        response = requests.get(
            url,
            auth=(self.username, self.password)
        )

        if response.ok:
            auth_data = json.loads(response.text or response.content)
            for auth in auth_data:
                print(json.dumps(auth, indent=4))
        else:
            print(json.dumps(response.json()['message'], indent=4))

    def delete_authorization(self, auth_id):
        url = urljoin(self.GITHUB_API, 'authorizations/' + auth_id)
        response = requests.delete(
            url,
            auth=(self.username, self.password),
        )

        if response.ok:
            print('Successful delete')
        else:
            print(json.dumps(response.json()['message'], indent=4))

    # latest id: since 115891102
    def get_all_repositories(self, token, since):
        repos_url = urljoin(self.GITHUB_API, 'repositories')
        # the token must be included in header
        head = {'Authorization': 'token %s' % token}
        # since variable define the start id of the repository
        params = {'since': since}
        response = requests.get(
            repos_url,
            headers=head,
            params=params
        )
        # res = requests.get('https://api.github.com/repositories', params=params)
        if response.ok:
            repos_data = json.loads(response.text or response.content)
            return repos_data
        else:
            print(json.dumps(response.json()['message'], indent=4))
            error = 'request error'
            return error

    def get_repository_details(self, token, url):
        head = {'Authorization': 'token %s' % token}
        response = requests.get(
            url,
            headers=head
        )

        if response.ok:
            repos_detail = json.loads(response.text or response.content)
            return repos_detail
        else:
            # print(json.dumps(response.json()['message'], indent=4))
            error = 'not found'
            return error

    def search_latest_repositories(self, token, page):
        search_repos_url = urljoin(self.GITHUB_API, '/search/repositories')
        head = {'Authorization': 'token %s' % token}
        params = {'q': 'created:2018-01-01', 'page': page, 'per_page': 100}
        response = requests.get(
            search_repos_url,
            headers=head,
            params=params
        )

        if response.ok:
            searched_data = json.loads(response.text or response.content)
            return searched_data
        else:
            print(json.dumps(response.json()['message'], indent=4))
            error = 'request error'
            return error


if __name__ == '__main__':
    username = input('GitHub username: ')
    password = input('GitHub password: ')
    # password = getpass.getpass('GitHub password: ')

    # win_unicode_console.enable()
    df = DataFetching(username, password)
    df.generate_authorization('your authorization name')  # define a arbitrary name for it to identify
    df.get_authorization('one of your authorization ids')
    df.list_all_authorization()
    token = 'your token'

    since = 115891102
    # since = -1
    for i in range(0, 1):
        all_repos = df.get_all_repositories(token, since)
        # repos_data = r.json()
        if all_repos != 'request error':
            for repos in all_repos:
                detail = df.get_repository_details(token, repos['url'])
                if detail != 'not found':
                    print(json.dumps(detail, indent=4))
                else:
                    continue

            since = all_repos[-1]['id']
        else:
            break

    # for i in range(0, 1):
    #     searched_data = df.search_latest_repositories(token, i)
    #     if searched_data != 'request error':
    #         for repos in searched_data['items']:
    #             print(json.dumps(repos, indent=4))
    #
    #     else:
    #         break
