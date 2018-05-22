CSV_FIELDNAMES = ('rank', 'athlete_name', 'start_date', 'start_date_local', 'elapsed_time', 'moving_time')

try:
    from local_config import *
except ImportError:
    pass

STRAVA_API_KEY = '7ccf3e6508023869334797d22ba8fdace3d52a04'

STRAVA_SEGMENT_LEADERBOARD_URL = 'https://www.strava.com/api/v3/segments/{}/leaderboard'


class AthletheConfig:
    AGE_CLASS = {0: '0_19', 20: '20_24', 25: '25_34', 35: '35_44', 45: '45_54', 55: '55_64', 65: '65_69', 70: '70_74',
                 75: '75_plus'}
    WEIGHT_CLASS = {
        0: '0_124', 125: '125_149', 150: '150_164', 165: '165_179', 180: '180_199',
        200: '200_224', 225: '225_249', 250: '250_plus'
    }
    WEIGHT_SCALE = [0, 125, 150, 165, 180, 200, 250]
    AGE_SCALE = [0, 20, 35, 45, 55, 65, 70, 75]

    @classmethod
    def validate_weight(cls, weight):
        """
        Returns weight range for according to weight param
        :param weight: in lbs
        :return: weight category as query param
        """
        try:
            weight_int = int(weight)
            try:
                goal_weight = next(filter(lambda x: x > weight_int, AthletheConfig.WEIGHT_SCALE))
            except StopIteration:
                goal_weight = AthletheConfig.WEIGHT_SCALE[-1]
            return AthletheConfig.WEIGHT_CLASS[goal_weight]
        except ValueError:
            raise RuntimeError(f'The value of weight - {weight} - is not valid')

    @classmethod
    def validate_age(cls, age):
        """
        Returns weight range for according to weight param
        :param weight: in lbs
        :return: weight category as query param
        """
        try:
            age_int = int(age)
            try:
                goal_age = next(filter(lambda x: x > age_int, AthletheConfig.AGE_CLASS))
            except StopIteration:
                goal_age = AthletheConfig.WEIGHT_SCALE[-1]
            return AthletheConfig.AGE_CLASS[goal_age]

        except ValueError:
            raise RuntimeError(f'The value of age - {age} - is not valid')

    @classmethod
    def validate_params(cls, age=None, weight=None):
        return {'age_group': cls.validate_age(age) if age is not None else None,
                'weight_class': cls.validate_weight(weight) if weight is not None else None}


ADDITIONAL_HEADERS = {'Authorization': 'Bearer {}'.format(STRAVA_API_KEY),
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0', }

if __name__ == '__main__':
    print(AthletheConfig.validate_weight(260))
