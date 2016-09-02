from tinderclient import TinderClient
import time


SWIPE_DELAY = 0.25
GET_NEARBY_USERS_DELAY = 5

facebook_token = ''
facebook_id = ''

tinder = TinderClient(facebook_token, facebook_id)
print "Logged in as " + tinder.full_name

print "Swiping right on users within " + tinder.distance_filter + " miles..."
matches = []

while True:
    nearby_users = tinder.nearby_users()
    if 'message' in nearby_users:
        if 'message' == 'recs exhausted':
            print "Ran out of people to swipe."
            break

    for userItem in nearby_users['results']:
        for user in userItem['user']:
            swipe = tinder.swipe_right(user['_id'])
            if swipe['match']:
                photos = []
                for photo in user['photos']:
                    photos.append(photo['url'])

                common_interests = []
                for interest in user['common_interests']:
                    common_interests.append(interest['name'])

                match = {
                    'name': user['name'],
                    'bio': user['bio'],
                    'photos': photos,
                    'common_interests': common_interests
                }
                matches.append(match)

            if swipe['likes_remaining'] == 0:
                print "Used all likes. Come back on " + time.strftime('%b %d at %l:%M%p')
                break

            time.sleep(SWIPE_DELAY)

    time.sleep(GET_NEARBY_USERS_DELAY)

