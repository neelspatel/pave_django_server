import facebook
import datetime
import json
import requests
import time

url = "http://ec2-54-218-218-2.us-west-2.compute.amazonaws.com/data/updatetopfriends"
def get_top_friends(oauth):
	#oauth = "CAACEdEose0cBAE7AQRa3gbHKMdx97pNRh9rapZBCivsZCwqkiUZA7UqHv92sepsHYJagOXESFwa0NGBTrRRQNy0RhxZCN3fOats2ciXJ9FXY1DR2ugjIgok6Jq9WLciiIUVdZC3wvLvIvrSR6HttL5LbACo1DgY5ZAluXO0gkLmwZDZD"
	graph = facebook.GraphAPI(oauth)
	data = graph.fql({"posts": "select actor_id, post_id from stream where source_id = me() and likes.count > 0 limit 200",
				"friends_who_like_posts":"select user_id FROM like WHERE post_id IN (SELECT post_id FROM #posts) AND user_id IN (SELECT uid2 FROM friend WHERE uid1 = me() )",
				"friends_who_commented": "select fromid FROM comment WHERE post_id IN (SELECT post_id FROM #posts) AND fromid IN (SELECT uid2 FROM friend WHERE uid1 = me())"
			})
	friend_scores = {}
	#posts authors 
	#print data[0]
	post_authors = data[0]["fql_result_set"]
	for post in post_authors:
		try:
			friend_scores[post["actor_id"]] += 10
		except KeyError:
			friend_scores[post["actor_id"]] = 10
		
	# people who commented
	#print data[1]
	comment_authors = data[1]["fql_result_set"]
	for comment in comment_authors:
		try:
			friend_scores[comment["fromid"]] += 5
		except KeyError:
			friend_scores[comment["fromid"]] = 5

	# people who liked
	#print data[2]	
	liked_authors = data[2]["fql_result_set"]
	for like in liked_authors:
		try:
			friend_scores[like["user_id"]] += 1
		except:
			friend_scores[like["user_id"]] = 1
	
	sorted_friends  = sorted(friend_scores.iteritems(), key=lambda (k,v): (v,k), reverse = True)
	print sorted_friends
	#user_id = "551733910"
	#full_url = url + "/" + user_id + "/"
	#r = requests.post(full_url, data={"data": json.dumps(sorted_friends)})
	#print r.text

	#for friend, score in sorted_friends:
	#	profile = graph.get_object(str(friend))
	#	print "%s %s %s" % (profile["first_name"], profile["last_name"], str(score))		

def get_friends(oauth):
	graph = facebook.GraphAPI(oauth)
	data = graph.fql("SELECT uid, name, sex FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) ORDER BY mutual_friend_count DESC")
	print data

def get_profile(oauth):
	graph = facebook.GraphAPI(oauth)
	profile = graph.get_object("me")
	print profile

