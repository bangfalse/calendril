# calendril

A really stupid project which creates Google calendar events from random recent tweets on a Twitter feed.

## Why?

One morning I woke up with the word "canlendril" in my head.

As [Professor Hubert J. Farnsworth](http://futurama.wikia.com/wiki/Hubert_J._Farnsworth) once said:
> It came to me in a dream, and I forgot it in another dream

... but I only forgot what the meaning of the word was, not the word itself. So I mentally defined as "a calendar full of [dril](https://twitter.com/dril) tweets". And then I decided to actually do it.

## What if I just want the calendar, not the code?

I've posted a [public calendar](https://calendar.google.com/calendar/b/1?cid=cHJvZmVzc2lvbmFsbHlyaWRpY3Vsb3VzLmNvbV80bnFsMnY5Z3Vkb3V1NDluMGJka3N0aWdzOEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t). You can add this to your own Google Calendar for your daily dose of dril, up through 2024-09-02.

## Limitations

This can only create as many calendar events as it can access Tweets via the API, which is limited to 3200 (including native retweets). I have excluded retweets, so it could be quite a bit less in reality.

## Instructions for use

I assume you know how to clone this git repo. You'll need python 3.x installed, and you should probably run this in a [venv](https://docs.python.org/3/library/venv.html) to not install packages globally for this garbage. Once you're in there:

- Run `pip install -r requirements.txt`
- Go to <https://apps.twitter.com> and set up a new app
	- Once you've created the new app, click over to the `Keys and Access Tokens` tab
	- Click the `Create my access token` button to create your personal access token for this new app
- Enable the Google Calendar API using the [Google API wizard](https://console.developers.google.com/start/api?id=calendar), creating a new Google project if necessary
	- Click the `Go to credentials` button
	- Choose `Google Calendar API` and `Other UI` from the dropdowns, and `User data` from the radio buttons
	- Go through the wizard and create an OAuth 2.0 client ID
	- Download the `client_id.json` file or navigate to your client secret 
- Edit `config.json` to include:
	- The Twitter account whose tweets you wish to use
	- Your Twitter credentials
	- Your Google credentials
	- If you have an existing calendar you want to use, find its ID (available in `Settings & Sharing` for the calendar), and put it in the `calendar_id` field in `config.json`
	- If you don't have an existing calendar, the title you want for your new calendar
- Run `calendril.py`
	- The first time you run this, the Google API integration should kick you to a web page to authorize the app - if you run it again for some reason, the credentials will be cached

There's basically no error handling in here, but something should blow up on an API call if you don't fill in a config value correctly or something bad happens.

