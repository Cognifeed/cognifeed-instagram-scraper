import time
from urllib.request import urlopen
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs


class InstagramScraper:

  def __init__(self, chrome_driver_path, headless=True):
    chrome_options = Options()
    if headless:
      chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    self.browser = webdriver.Chrome(
        chrome_driver_path, chrome_options=chrome_options)

  def get_posts_from_user(self,
                          username,
                          number_of_posts=50,
                          wait_for_scroll=1.0):
    self.browser.get('https://www.instagram.com/' + username + '/?hl=en')
    links = []
    last_page_length = 0
    while len(links) < number_of_posts:
      page_length = self.browser.execute_script(
          "window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(wait_for_scroll)
      if page_length == last_page_length:
        break
      last_page_length = page_length
      try:
        source = self.browser.page_source
        data = bs(source, 'html.parser')
        body = data.find('body')
        script = body.find('span')
        for link in script.findAll('a'):
          link = 'https://www.instagram.com' + link.get('href')
          if not link in links and '/p/' in link:
            links.append(link)
      except:
        pass
    if number_of_posts < len(links):
      number_of_posts = len(links)
    return links[:number_of_posts]

  def get_data(self, post_links, retries=5):
    posts_data = {}
    for post_link in post_links:
      successfully_opened = False
      no_tries = 0
      while not successfully_opened and no_tries <= retries:
        try:
          no_tries += 1
          page = urlopen(post_link).read()
          successfully_opened = True
          data = bs(page, 'html.parser')
          body = data.find('body')
          script = body.find('script')
          raw = script.text.strip().replace('window._sharedData =', '').replace(
              ';', '')
          json_data = json.loads(raw)
          if 'PostPage' not in json_data['entry_data']:
            continue
          post_data = json_data['entry_data']['PostPage'][0]['graphql'][
              "shortcode_media"]

          is_video = post_data["__typename"] == "GraphVideo"
          posts_data[post_data["shortcode"]] = {
              "media":
              post_data["thumbnail_src"]
              if is_video else post_data["display_url"],
              "caption":
              post_data["edge_media_to_caption"]["edges"][0]['node']['text'],
              "comments":
              post_data["edge_media_preview_comment"]["count"]
              if "edge_media_preview_comment" in post_data else 0,
              "likes":
              post_data["edge_media_preview_like"]["count"]
              if "edge_media_preview_like" in post_data else 0,
              "username":
              post_data["owner"]["username"],
              "shortcode":
              post_data["shortcode"]
          }
        except:
          print("Oops. Something went wrong, trying again.")

    return posts_data


# directory = "/directory/you/want/to/save/images/"
# for i in range(len(result)):
#   r = requests.get(result['display_url'][i])
#   with open(directory + result['shortcode'][i] + ".jpg", 'wb') as f:
#     f.write(r.content)

# print(result.iloc[0]["edge_media_to_caption.edges"][0]['node']['text'])
