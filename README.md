# LocalSocial
LocalSocial is an open source self hosted tool that takes care of all your social media activities under one place.From posting to editing to scheduling on different platforms,you get to do all of these activities by self hosting it right on your local environment.

 LocalSocial  works with twitter on which you get to:-
- create tweets 
- delete tweets
- edit tweets

 LocalSocial now works with reddit on which you can get to:-
 - submit posts on your subreddits
 - edit the posts
 - delete the posts

Platforms like Linkedin,~~reddit~~,facebook,hacker news will soon be added.

# Requirements
- Python 3.6 or higher
- Flask
- Sqlite

# Getting started
- clone the repository `git clone https://github.com//Saptarshi2001/LocalSocial.git`
- Go to the [twitter developer platform](https://developer.x.com/en) 
- Get the credentials of your application  for authorization such as consumer_key,consumer_secret,access_token,access_secret,bearer_token
- create a setup.py file and put these credentials over there.
- use these credentials to create the twitter client `api = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_secret
)`
- - Go to the [reddit developer platform](https://www.reddit.com/dev/api/) 
- Get the credentials of your application  for authorization such as client_id,client_secret,username and reddit password
- create a setup.py file and put these credentials over there.
- use these credentials to create the reddit client `reddit=praw.Reddit(client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
            )
`
- 
- Go to the terminal and enter `flask --app LocalSocial run`
- Go to the browser and enter `127.0.0.1:5000/socials` and you get 

# Roadmap

There's honestly a lot of things to improve on this software.Here are the ones that will be the key focus as of now:-

- A message queue to schedule posts for a specific time and date
- Support on platforms such as Linkedin,~~reddit~~ and facebook
- Improving the ui by creating a seperate page that shows all the posts being posted

# Contributing

This project is under development.Feel free to contribute to it

