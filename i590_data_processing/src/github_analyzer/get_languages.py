import requests
import json
from urllib.parse import urljoin

class GetLanguages:
    def __init__(self):
        self.GITHUB_API = 'https://api.github.com'  # basic api address

    def get_languages(self, token, repo):
        get_lang_url = urljoin(self.GITHUB_API, '/repos/' + repo)
        head = {'Authorization': 'token %s' % token}
        response = requests.get(
    		get_lang_url,
    		headers=head
    	)
        if response.ok:
            languages = json.loads(response.text or response.content)
            return languages
        else:
            print(json.dumps(response.json()['message'], indent=4))
            error = 'request error'
            return error


if __name__ == '__main__':

    gl = GetLanguages()
    token = '85015b14f0ff000b5ace4789c0de0e6a9f4c39b6'

    # Call function to get languages data for each repository
    searched_data = gl.get_languages(token, "kelseyhightower/echo/languages")
    if searched_data != 'request error' and searched_data != 'date invalid':
            print(searched_data)


