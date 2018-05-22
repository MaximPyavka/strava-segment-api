import requests
from operator import itemgetter

from config import ADDITIONAL_HEADERS, STRAVA_SEGMENT_LEADERBOARD_URL, CSV_FIELDNAMES, AthletheConfig
from file_handler import CSVWriterContextManager


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
            obj.session.headers.update(ADDITIONAL_HEADERS)
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
        try:
            segm_id = int(segm_id)
        except ValueError:
            print('Segm_id value {} is invalid'.format(segm_id))
        finally:
            return func(*args, **kwargs)

    return wrapper


class StravaClient:
    """
    StravaApi client
    """
    segment_lead_init_params = {'per_page': 200, 'page': 1}

    def __init__(self):
        self.session = None

    @check_session
    @check_segment_id
    def parse_segments_leaderboard(self, segment_id, age_group=None, weight_class=None):
        effort_count = self.get_effort_count(segment_id)
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
    def get_effort_count(self, segment_id, **kwargs):
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
            for n, athlete_info in enumerate(self.parse_segments_leaderboard(segment_id, age_group=age_group,
                                                                             weight_class=weight_class)):
                print(n)
                self.write_athlete(athlete_info, out_file)


if __name__ == '__main__':
    segm = '7601651'
    age = None
    weight = None

    conf = AthletheConfig.validate_params(age=age, weight=weight)

    client = StravaClient().generate_athletes_to_csv(segment_id=segm, **conf)
