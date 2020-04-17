import requests
import json
import sys

GRAPH_API_URL = "https://graph.facebook.com/v2.10/"

def page_scrapper(page, access_token):
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
            reachs.append(data_insights["data"][0]["values"][0]["value"])

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

    for i in range(0,len(ids)):
        print str(time[i]) + "," + "https://www.facebook.com/"+str(ids[i]) + "," + str(likes[i]) + "," + str(comments[i]) + "," + str(shares[i]) + "," + str(reachs[i])
