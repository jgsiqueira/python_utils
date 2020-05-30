import requests
import json
import sys

GRAPH_API_URL = "https://graph.facebook.com/"

#
# You need an app published with the permissions listed on each method to access pages you don't own
# If you want to just check your own page, you can get a page token in https://developers.facebook.com/tools/explorer/
#
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"

def get_fb_token(app_id, app_secret):
    url = 'https://graph.facebook.com/oauth/access_token'       
    payload = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret
    }
    response = requests.post(url, params=payload)
    return response.json()['access_token']

#
# Necessary permissions: pages_read_engagement
#
def get_page_top_posts(page, access_token):
    page_info_url = GRAPH_API_URL + page + "?fields=fan_count&access_token=" + access_token
    feed_url = GRAPH_API_URL + page + "/feed?fields=shares,comments.limit(0).summary(true),reactions.limit(0).summary(true),created_time&access_token=" + access_token

    r = requests.get(page_info_url)
    data = json.loads(r.text)

    numberOfLikes = data["fan_count"]

    r = requests.get(feed_url)
    data = json.loads(r.text)

    posts = data["data"]

    likes = []
    comments = []
    shares = []
    ids = []
    time = []
    reachs = []

    while len(posts) > 0:
        for post in posts:
            ids.append(post["id"])
            time.append(post["created_time"])

            post_reach_url = GRAPH_API_URL + post["id"] + "/insights/post_impressions_unique?access_token=" + access_token

            r_insights = requests.get(post_reach_url)
            data_insights = json.loads(r_insights.text)

            if len(data_insights["data"]) > 0:
                reachs.append(data_insights["data"][0]["values"][0]["value"])
            else:
                reachs.append(0)

            if ("reactions" in post) and ("summary" in post["reactions"]):
                likes.append(post["reactions"]["summary"]["total_count"])
            else:
                likes.append(0)

            if ("comments" in post) and ("summary" in post["comments"]):
                comments.append(post["comments"]["summary"]["total_count"])
            else:
                comments.append(0)

            if ("shares" in post):
                shares.append(post["shares"]["count"])
            else:
                shares.append(0)

        if "next" in data["paging"]:
            r = requests.get(data["paging"]["next"].replace("limit=25","limit=100"))
            data = json.loads(r.text)
            posts = data["data"]
        else:
            posts = []

    # Wrap the result in a single dict
    result = {}

    for i in range(0,len(ids)):
        result[ids[i]] = {}
        result[ids[i]]["likes"] = likes[i]
        result[ids[i]]["comments"] = comments[i]
        result[ids[i]]["shares"] = shares[i]
        result[ids[i]]["reachs"] = reachs[i]

    return result

#
# Necessary permissions: pages_read_engagement
#
def get_post_details(post_id):
    post_url = GRAPH_API_URL + post_id + "?fields=message,attachments&access_token=" + access_token

    r = requests.get(post_url)
    data = json.loads(r.text)

    print(data)

#
# Necessary permissions: pages_read_engagement, pages_manage_posts
#
def publish_post(page, message):
    page_url = GRAPH_API_URL + page + "/feed?access_token=" + access_token
    
    post_data = {}
    post_data["message"] = message

    r = requests.post(page_url, data=post_data)
    data = json.loads(r.text)

    print(data)
