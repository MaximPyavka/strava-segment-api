import requests

from config import ADDITIONAL_HEADERS, STRAVA_SEGMENT_LEADERBOARD_URL


def check_session(func):
    """
    Decorator for web_client functions to use one session
    :param func: function to use session
    :return: web client function
    """

    def wrapper(*args):
        obj = args[0]
        if obj.session is None:
            obj.session = requests.Session()
            obj.session.headers.update(ADDITIONAL_HEADERS)
        return func(*args)

    return wrapper


def check_segment_id(func):
    """
    Checks segment_id value
    :param func: function to use session
    :return: web_client_function
    """

    def wrapper(*args):
        segm_id = args[1]
        try:
            segm_id = int(segm_id)
        except ValueError:
            print('Segm_id value {} is invalid'.format(segm_id))
        else:
            return func(*args)
        return func(*args)

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
    def parse_segments_leaderboard(self, segment_id):
        effort_count = self.get_effort_count(segment_id)
        if not effort_count:
            print('No athletes found on this segment')

        params = {k: v for k, v in StravaClient.segment_lead_init_params.items()}
        url = STRAVA_SEGMENT_LEADERBOARD_URL.format(segment_id)

        while effort_count > 0:
            resp = self.session.get(url, params=params)
            entries = resp.json().get('entries', [])
            if entries:
                params['page'] +=1
                pass
            else:
                break

    @check_session
    def get_effort_count(self, segment_id):
        get_effort_response = self.session.get(
            STRAVA_SEGMENT_LEADERBOARD_URL.format(segment_id)
        )
        _json = get_effort_response.json()
        eff_count = _json.get('effort_count', 0)
        return eff_count
