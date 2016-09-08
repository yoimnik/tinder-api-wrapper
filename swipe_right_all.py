from tinderclient import TinderClient
from tinder_token import facebook_id, facebook_token
import datetime
import time


SWIPE_DELAY = 0.25
GET_NEARBY_USERS_DELAY = 5

tinder = TinderClient(facebook_token, facebook_id)
print "Logged in as " + tinder.full_name

print "Swiping right on users within " + `tinder.distance_filter` + " miles..."
matches = []
while True:
    nearby_users = tinder.nearby_users()
    if 'message' in nearby_users:
        if 'message' == 'recs exhausted':
            print "Ran out of people to swipe."
            break

    has_swipes = True
    for user in nearby_users['results']:
        swipe = tinder.swipe_right(user['_id'])
        if swipe['match']:
            schools = []
            for school in user['schools']:
                schools.append(school['name'])

            common_interests = []
            if 'common_interests' in user:
                for interest in user['common_interests']:
                    common_interests.append(interest['name'])

            photos = []
            for photo in user['photos']:
                photos.append(photo['url'])

            match = {
                'name': user['name'],
                'bio': user['bio'],
                'schools': schools,
                'common_interests': common_interests,
                'photos': photos
            }
            matches.append(match)

        if swipe['likes_remaining'] == 0:
            seconds = swipe['rate_limited_until'] / 1000.0
            more_likes_time = datetime.datetime.fromtimestamp(seconds)
            formatted_time = more_likes_time.strftime("%b %d at %l:%M%p")
            print "Used all likes. Will have more on " + formatted_time + "."
            has_swipes = False
            break

        time.sleep(SWIPE_DELAY)

    if not has_swipes:
        break
    else:
        time.sleep(GET_NEARBY_USERS_DELAY)

print "Matches:"
if matches:
    output = []
    for match in matches:
        info = "Name: " + match['name'] + "\n" + \
               "Bio: " + match['bio'] + "\n" + \
               "Schools: " + ', '.join(match['schools']) + "\n" + \
               "Common Interests: " + ', '.join(match['common_interests']) + "\n"

        urls = "\n".join(match['photos'])

        output.append(info + urls + "\n")

    print "\n".join(output)
else:
    print "None."
