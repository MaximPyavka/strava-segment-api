import requests
from lxml import html
from operator import itemgetter

from config import ADDITIONAL_HEADERS, STRAVA_SEGMENT_LEADERBOARD_URL, CSV_FIELDNAMES, AUTH_DATA, \
    STRAVA_LOGIN, STRAVA_SESSION
from file_handler import CSVWriterContextManager


def get_auth_token(session):
    r = session.get(STRAVA_LOGIN).text
    parser = html.fromstring(r)
    token = parser.xpath("//input[@name='authenticity_token']/@value")[0]
    return token


def check_session(func):
    """
    Decorator for web_client functions to use one session
    :param func: function to use session
    :return: web client function
    """

    def wrapper(*args, **kwargs):
        obj = args[0]
        if obj.session is None:
            obj.session = requests.Session()
            AUTH_DATA['authenticity_token'] = get_auth_token(obj.session)
            obj.session.headers.update(ADDITIONAL_HEADERS)
            obj.session.post(STRAVA_SESSION, data=AUTH_DATA)
        return func(*args, **kwargs)

    return wrapper


def check_segment_id(func):
    """
    Checks segment_id value
    :param func: function to use session
    :return: web_client_function
    """

    def wrapper(*args, **kwargs):
        segm_id = args[1]
        while not segm_id.isdigit():
            segm_id = input("Please try again, and type valid segment id number...\n")
            continue
        else:
            args = (args[0], segm_id) + args[2:]
            return func(*args, **kwargs)

    return wrapper


class StravaClient:
    """
    StravaApi client
    """
    segment_lead_init_params = {'per_page': 200, 'page': 1}

    def __init__(self):
        self.session = None
        self.save_headers = []

    @check_session
    @check_segment_id
    def parse_segments_leaderboard_api(self, segment_id, age_group=None, weight_class=None):
        effort_count = self.get_effort_count_api(segment_id)
        print(effort_count)
        if not effort_count:
            print('No athletes found for this segment')

        params = {k: v for k, v in StravaClient.segment_lead_init_params.items()}
        params['age_group'] = age_group
        params['weight_class'] = weight_class

        url = STRAVA_SEGMENT_LEADERBOARD_URL.format(segment_id)

        while effort_count > 0:
            print(params)
            resp = self.session.get(url, params=params)
            resp_dict = resp.json()
            entries = resp_dict.get('entries', [])
            print(len(entries))
            if entries:
                yield from sorted(entries, key=itemgetter('rank'))
                effort_count -= params['per_page']
                params['page'] += 1
            else:
                break

    @check_session
    def get_effort_count_api(self, segment_id, **kwargs):
        get_effort_response = self.session.get(
            STRAVA_SEGMENT_LEADERBOARD_URL.format(segment_id),
            params=kwargs
        )
        _json = get_effort_response.json()
        eff_count = _json.get('effort_count', 0)
        return eff_count

    def write_athlete(self, athlete_info, csv_file):
        csv_file.writerow(athlete_info)

    def generate_athletes_to_csv(self, segment_id, age_group=None, weight_class=None):
        with CSVWriterContextManager('athletes.csv', CSV_FIELDNAMES) as out_file:
            for n, athlete_info in enumerate(self.parse_segments_leaderboard_api(segment_id, age_group=age_group,
                                                                                 weight_class=weight_class)):
                print(n)
                self.write_athlete(athlete_info, out_file)

    @check_session
    @check_segment_id
    def get_leaderboard_by_segment(self, segment_id):
        self.save_headers = dict(self.session.headers)
        # leaders = self.get_leader_html(segment_id)

        params = {
            'filter': 'overall',
            'page': 1,
            'per_page': 25,
            'partial': 'true'
        }

        self.session.headers = {'Cookie': self.session.headers.get('Cookie')}

        filename = f'athletes_{segment_id}.csv'

        with CSVWriterContextManager(filename, CSV_FIELDNAMES) as out_file:
            while True:
                res = self.session.get(f'https://www.strava.com/segments/{segment_id}/leaderboard', params=params)
                data = self.get_athletes_html(res)
                for n, d in enumerate(data):
                    if len(d) == 1 or d is None:
                        if params['page'] == 1:
                            print(f'No athletes found for segment ID {segment_id}')
                        print(f"Done, please check file --> '{filename}'")
                        return
                    print(f'Searching for athlete number {n+1+(params["page"]-1)*params["per_page"]}...')
                    out_file.writerow(d)
                params['page'] += 1

    def get_athletes_html(self, response):
        if response.status_code == 200:
            parser = html.fromstring(response.text)
            data = parser.xpath('//table[contains(@class, "table-leaderboard")]//tbody//tr')
            if not data:
                yield (None, )
            for d in data:
                yield [d for d in d.xpath('string(.)').split('\n') if d]
        else:
            print('No segments found for this Id')

    def get_leader_html(self, segment_id):
        res = self.session.get(f'https://www.strava.com/segments/{segment_id}')
        html_body = html.fromstring(res.text)
        leaders = html_body.xpath('//div[@class="result"]//div[@class="athlete"]//text()')
        return leaders
