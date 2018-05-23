import requests
from lxml import html
from config import ADDITIONAL_HEADERS

if __name__ == '__main__':
    data = {
        'authenticity_token': '',
        'email': 'hello@veercycle.com',
        'password': 'temporarypasswordfornikita',
        'utf8': '✓',
        'plan': '',
    }
    url = 'https://www.strava.com/login'

    s = requests.Session()
    s.headers.update(ADDITIONAL_HEADERS)
    r = s.get('https://www.strava.com/login').text
    parser = html.fromstring(r)

    token = parser.xpath("//input[@name='authenticity_token']/@value")[0]
    print(token)

    data['authenticity_token'] = token

    r = s.post('https://www.strava.com/session', data=data)

    res = s.get('https://www.strava.com/segments/7601651/leaderboard?filter=overall&page=2&per_page=25')
    print(res, res.text)