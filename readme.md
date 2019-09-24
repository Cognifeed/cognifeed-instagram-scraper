Instagram Post Scraper
=
The aim of this scraper is to get instagram post data that can be used in Cognifeed to teach a machine learning algorithm to predict various attributes about the post.

This scrapper is used in our Medium article that highlights how brands can use Cognifeed to find the perfect influencer for their influencer marketing campain. Check it out here.

Requirements
-
To install the python requirements run:

`pip install -r requirements.txt`

You also need to install **Chromedriver** by following instructions here: http://chromedriver.chromium.org/downloads

Extract the binary in a folder, and remember the path.

Oh... and if you don't already, you need to have Chrome installed.

Using the scraper
-
First, you need to make a list of instagram accounts that you want to scrape. You can either write them over `lists/influencers.txt`, which is the default file that's loaded. You can also save them in a separate file to which we will point the program later.

To run the scraper use the following command:
```
python main.py [-h] [--username_list USERNAME_LIST_PATH]
               [--chromedriver_path CHROMEDRIVER_PATH] [--out_file OUT_FILE]
```

Where:
* `USERNAME_LIST_PATH` is the path to the file you've crated containing influencers' usernames.
* `CHROMEDRIVER_PATH` is the path to your chromedriver binary file (the folder we've asked you to remember earlier).
* `OUT_FILE` is the path to the file where you want to save the data scraped from instagram.

Example:
```
python main.py --username_list ./lists/shortlist.txt --chromedriver_path ./chromedriver.exe --out_file dataset_v1.csv
```