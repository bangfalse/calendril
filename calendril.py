#!/usr/bin/env python

import tweepy
import json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import random
from datetime import datetime, timedelta


def main():
    config = json.load(open("config.json"))
    user = config["twitter"]["user"]

    twitter_api = get_twttier_api(config)
    service = get_calendar_service(config)

    print("Getting tweets for user %s" % user)
    tweets = get_tweets(twitter_api, user)
    print("Got %d tweets total to make events for!" % len(tweets))

    calendar_id = config["google"]["calendar_id"]
    if calendar_id is None:
        print("Creating new calendar...")
        calendar_id = create_calendar(service, config["google"]["calendar_name"])

    print("Will put events on calendar %s..." % calendar_id)
    event_date = datetime.utcnow() - timedelta(days=1)

    batch = service.new_batch_http_request()
    batch_count = 0

    random.shuffle(tweets)
    for tweet in tweets:
        tweet_url = "https://twitter.com/%s/status/%s" % (user, tweet.id_str)
        event_date += timedelta(days=1)
        date_str = event_date.strftime("%Y-%m-%d")
        print("\r  Creating event for %s..." % date_str, end="")
        request = service.events().insert(calendarId=calendar_id, body={
            "summary": tweet.text,
            "description": tweet_url,
            "start": {
                "date": date_str,
                "timeZone": "UTC"
            },
            "end": {
                "date": date_str,
                "timeZone": "UTC"
            },
            "guestsCanSeeOtherGuests": False,
            "guestsCanModify": False,
            "transparency": "transparent"
        })
        batch.add(request)
        batch_count += 1
        if batch_count == 1000:
            send_batch(batch, batch_count)
            batch_count = 0

    if batch_count > 0:
        send_batch(batch, batch_count)

    print()
    print("Done!")


def send_batch(batch, batch_count):
    print()
    print("  Sending batched request to create %d events..." % batch_count)
    batch.execute()


def get_twttier_api(config):
    auth = tweepy.OAuthHandler(config["twitter"]["consumer_key"], config["twitter"]["consumer_secret"])
    auth.set_access_token(config["twitter"]["access_token"], config["twitter"]["access_token_secret"])
    return tweepy.API(auth)


def get_tweets(api, user):
    alltweets = []
    new_tweets = api.user_timeline(screen_name=user, count=200, trim_user=True, include_rts=False, exclude_replies=True)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=user, count=200, trim_user=True, include_rts=False, exclude_replies=True, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print("\r  Got %d tweets so far..." % len(alltweets), end="")

    print()
    return alltweets


def get_calendar_service(config):
    store = file.Storage("credentials.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.OAuth2WebServerFlow(
            config["google"]["client_id"],
            client_secret=config["google"]["client_secret"],
            scope="https://www.googleapis.com/auth/calendar")
        creds = tools.run_flow(flow, store)

    return build("calendar", "v3", http=creds.authorize(Http()))


def create_calendar(service, name):
    calendar = service.calendars().insert(body={
        "summary": name,
        "description": "Tweets by %s" % name
    }).execute()
    return calendar["id"]


if __name__ == "__main__":
    main()
