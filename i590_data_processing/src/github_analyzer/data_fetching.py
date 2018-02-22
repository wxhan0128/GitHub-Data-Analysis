import requests
import json
from urllib.parse import urljoin


class DataFetching:
    def __init__(self, username, password):
        self.GITHUB_API = 'https://api.github.com'

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

    def get_all_repositories(self, token, since):
        repos_url = urljoin(self.GITHUB_API, 'repositories')
        # the token must be included in header
        head = {'Authorization': 'token %s' % token}
        # since variable define the start id of the repository
        params = {'since': since, 'per_page': 300}
        response = requests.get(
            repos_url,
            headers=head,
            params=params
        )
        # res = requests.get('https://api.github.com/repositories', params=params)

        return response


if __name__ == '__main__':
    username = input('GitHub username: ')
    password = input('GitHub password: ')
    token = 'your token'

    df = DataFetching(username, password)
    df.generate_authorization('authorization name')  # define a arbitrary name for it to identify
    df.get_authorization('authorization id')
    df.list_all_authorization()

    since = 0
    for i in range(0, 100):
        response = df.get_all_repositories(token, since)
        if response.ok:
            repos_data = json.loads(response.text or response.content)
            # repos_data = r.json()
            for repos in repos_data:
                print(json.dumps(repos, indent=4))

            since = repos_data[-1]["id"]
        else:
            print(response.json()['message'])
            break
