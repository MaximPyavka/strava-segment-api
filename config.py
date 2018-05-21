STRAVA_API_KEY = 'put your api key here'

STRAVA_SEGMENT_LEADERBOARD_URL = 'https://www.strava.com/segments/{}/leaderboard'
AGE_GROUPS = ('0_19', '20_24', '25_34', '35_44', '45_54', '55_64', '65_69', '70_74', '75_plus')

WEIGHT_CLASS = (
    '0_124', '125_149', '150_164', '165_179', '180_199', '200_224', '225_249', '250_plus', '0_54', '55_64', '65_74',
    '75_84', '85_94', '95_104', '105_114', '115_plus')


class AthlethesConfig:
    AGE_GROUPS = ('0_19', '20_24', '25_34', '35_44', '45_54', '55_64', '65_69', '70_74', '75_plus')
    WEIGHT_CLASS = {
        0: '0_124', 125: '125_149', 150: '150_164', 165: '165_179', 180: '180_199',
        200: '200_224', 225: '225_249', 250: '250_plus', 54: '0_54', 55: '55_64', 65: '65_74',
        75: '75_84', 85: '85_94', 95: '95_104', 105: '105_114', 115: '115_plus',
    }


try:
    from local_config import *
except ImportError:
    pass

ADDITIONAL_HEADERS = {'Authorization': 'Bearer {}'.format(STRAVA_API_KEY),
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0', }
