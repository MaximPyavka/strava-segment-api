import argparse
from parser import StravaClient


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', dest='segment', required=True, help="segment")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(f"Parsing data for segment #{args.segment}...")
    client = StravaClient().get_leaderboard_by_segment(args.segment)
