from scraper import InstagramScraper
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
    description='Scrapes instagram posts from given users.')

parser.add_argument(
    '--username_list',
    dest='username_list_path',
    default='./lists/influencers.txt',
    help='Path to the list of instagram accounts that you want scraped.')
parser.add_argument(
    '--chromedriver_path',
    dest='chromedriver_path',
    default='C:/Chromedriver/chromedriver.exe',
    help=
    'Path to Chromedriver binary. See http://chromedriver.chromium.org/getting-started'
)
parser.add_argument(
    '--out_file',
    dest='out_file',
    default='./dataset.csv',
    help=
    'The file in which the scraped info will be stored. You should name it \'filename.csv\''
)


def load_influencer_list(path):
  with open(path, 'r') as in_file:
    influencers = in_file.read().splitlines()
  return influencers


def save_data(posts_info, save_path):
  df = pd.DataFrame.from_dict(posts_info, orient='index')
  df.set_index('shortcode', inplace=True)
  df.to_csv(save_path, sep=',', encoding='utf-8')


def main():
  args = parser.parse_args()
  scraper = InstagramScraper(args.chromedriver_path)
  influencers = load_influencer_list(args.username_list_path)
  all_data = {}
  for i, influencer in enumerate(influencers):
    print("{}/{}: Getting {}'s posts...".format(i + 1, len(influencers),
                                                influencer))
    links = scraper.get_posts_from_user(influencer, 10)
    all_data.update(scraper.get_data(links))
  save_data(all_data, args.out_file)


if __name__ == "__main__":
  main()
