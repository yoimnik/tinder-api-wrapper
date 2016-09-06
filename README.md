# Tinder API sniffed and wrapped in Python

I sniffed the private Tinder API by using a web debugging proxy and mocking user scenarios on the app. By viewing the web traffic from my mobile device on the proxy, I was able to see both the HTTP requests and responses for any user scenario.

I wrapped the most relevant API calls in a python class `TinderClient`, which upon construction, authorizes an instance to use and make changes to your Tinder account.

## Sniffing your Facebook Token

In order to use `TinderClient`, you have to obtain a user authentication token from Tinder by providing your Facebook ID and Facebook Token.

The Facebook ID is easy enough, just head over to [findmyfbid](http://findmyfbid.com/) and paste in your Facebook profile URL.

To get your Facebook Token for Tinder, you're going to have to use a web debugging proxy. Proxies like [Fiddler](http://www.telerik.com/fiddler) and [Charles](https://www.charlesproxy.com/) work just fine for this. Basically what you have to do is connect your mobile device to the same network as your computer running the proxy, and then modify your mobile device's connection settings to use a proxy with the IP address of your computer and the port used by the proxy. You may need to download certificates onto your mobile device to permit traffic through the proxy.

Once your mobile device is hooked up to the proxy, open up Tinder and a series of API calls will be made to the host `https://api.gotinder.com`; the first of which will be `POST /auth`. Look into the request body to find:

    {
        'facebook_token': facebook_token,
        'facebook_id': facebook_id,
    }

You will need your `facebook_token` whenever you want to initiate an instance of `TinderClient`. **Do not publicize your `facebook_token`.** With it, anyone can act as you on Tinder. If you ever release it and need to change it, the only alternative I know is to delete the app from your Facebook account (which will delete your Tinder bio/matches) and to sign up on Tinder with your Facebook account again.

On a side note, if you take a look at the response body of the `POST /auth` request, you'll see a key called `X-Auth-Token`. The value of this is needed in all other HTTP request headers to the Tinder API. This token does expire after sometime, which is why the Facebook Token is needed get another authorized instance.

## TinderClient calls

The functions in the wrapper return JSONs of the response bodies.

#### `TinderClient(facebook_token, facebook_id)`
  * POST /auth
  * Initializes an instance by authenticating the user with the token and ID.
  * Exits if token and/or ID are incorrect, or for any 5xx error.

        {
            'token': '...',
            'globals': {...},
            'user': {
                'active_time': 'ISO8601'
                'create_date': 'ISO8601',
                'age_filter_min': NUM,
                'discoverable': BOOL,
                'full_name': '...',
                'api_token': '...',
                'connection_count': NUM,
                'squads_discoverable': BOOL,
                'interests': [
                    {
                        'created_time': 'ISO8601',
                        'name': '...',
                        'id': '...'
                    },
                    ...
                    }
                ],
                'bio': '...',
                'jobs': [
                    {
                        'company': {
                            'displayed': BOOL,
                            'id': '...',
                            'name': '...'
                        },
                        'title': {
                            'displayed': BOOL,
                            'id': '...',
                            'name': '...'
                        }
                    },
                    ...
                    }
                ],
                'distance_filter': NUM,
                'can_create_squad': BOOL,
                'gender_filter': NUM,
                'photos': [
                    {
                        'yoffset_percent': NUM,
                        'extension': '...',
                        'xoffset_percent': NUM,
                        'fbId': '...',
                        'fileName': '...',
                        'url': 'http://images.gotinder.com/USER_ID/FILENAME',
                        'ydistance_percent': NUM,
                        'id': '...',
                        'xdistance_percent': NUM,
                        'processedFiles': [
                            {
                                'url': 'http://images.gotinder.com/USER_ID/WIDTHxHEIGHT_FILENAME',
                                'width': NUM,
                                'height': NUM
                            },
                            ...
                            }
                        ]
                    },
                ],
                'ping_time': 'ISO8601',
                'schools': [
                    {
                        'displayed': BOOL,
                        'year': '...',
                        'type': '...',
                        'id': '...',
                        'name': '...'
                    },
                    ...
                    }
                ],
                'name': 'Niketan',
                'squads_only': BOOL,
                'gender': NUM,
                'username': '...',
                'photos_processing': BOOL,
                'age_filter_max': NUM,
                'birth_date': 'ISO8601',
                '_id': 'USERID'
            },
            'versions': {...}
        }

#### `popular_locations()`
  * GET /location/popular
  * Returns the top 10 locations where Tinder is used from most to least.

        {
            'status': 200,
            'results': [
                {
                    'locality': {
                        'long_name': 'Los Angeles',
                        'short_name': 'Los Angeles'
                    },
                    'country': {
                        'long_name': 'United States',
                        'short_name': 'US'
                    },
                    'lon': -118.2436849,
                    'administrative_area_level_2': {  
                        'long_name':u'Los Angeles County',
                        'short_name':u'Los Angeles County'
                    },
                    'administrative_area_level_1': {  
                        'long_name': 'California',
                        'short_name': 'CA'
                    },
                    'lat': 34.0522342
                },
                ...
            ]
        }

#### `fetch_updates()`
  * POST /updates
  * Returns any recent matches.

        {
            'matches': [
                {
                    '_id': 'MATCH_ID',
                    'messages': [
                        {
                            '_id': '...',
                            'match_id': 'MATCH_ID',
                            'to': '...',
                            'from': '...',
                            'message': '...',
                            'sent_date': 'ISO8601',
                            'created_date': 'ISO8601',
                            'timestamp': 'MICROSOFT_DATE_FORMAT'
                        },
                        ...
                        }
                    ],
                    'last_activity_date': 'ISO8601'
                },
                ...
                }
            ],
            'blocks': [],
            'lists': [],
            'deleted_lists': [],
            'last_activity_date': 'ISO8601'
        }

#### `profile_meta()`
  * GET /meta
  * Returns information about your profile.  

        {
            'status': 200,
            'rating': {
                'rate_limited_until': MICROSOFT_DATE_FORMAT,
                'likes_remaining': NUM,
                'super_likes': {
                    'resets_at': MICROSOFT_DATE_FORMAT,
                    'allotment': NUM,
                    'remaining': NUM,
                    'alc_remaining': NUM,
                    'new_alc_remaining': NUM
                }
            },
            'user': { (see POST /auth) }
        }

#### `nearby_users()`
  * GET /user/recs
  * Returns nearby users based on your set distance. Note that this API call costs a lot of time (there seems to be some expensive calculation on the serverside to generate nearby users), so it is important that you sleep out calls to this if you are scripting.

        {
            'status': 200,
            'results': [
                {
                    'type': 'user',
                    'user': {
                        'distance_mi': NUM,
                        'common_connections': [
                            'name': '...',
                            'id': '...'
                        ],
                        'connection_count': NUM,
                        'common_likes': [
                            {
                                'id': '...',
                                'name': '...'
                            },
                            ...
                            }
                        ],
                        'common_interests':[
                            {
                                'id': '...',
                                'name': '...'
                            },
                            ...
                            }
                        ],
                        'common_friends':[
                            {
                                'id': '...',
                                'name': '...'
                            },
                            ...
                            }
                        ],
                        'content_hash':'...',
                        '_id':'USER_ID',
                        'badges':[],
                        'bio':'...',
                        'birth_date': 'ISO8601',
                        'gender': NUM,
                        'name': '...',
                        'ping_time': 'ISO8601',
                        'photos': [ (see POST /auth) ],
                        'jobs': [ (see POST /auth) ],
                        'schools': [ (see POST /auth) ],
                        'birth_date_info': 'fuzzy birthdate active, not displaying real birth_date'
                    }
                },
                ...
                }
            ]
        }
        
#### `user_info(user_id)`
  * GET /user/{user_id}
  * Returns information on the user
  * Same JSON format as GET /user/recs `'user'` key.

#### `swipe_right(user_id)`
  * POST /like/{user_id}
  * Likes the specified user.
  * When likes are remaining:
        
        {
            'match': BOOL,
            'likes_remaining': 100  // it will always be 100 while you have some
        }

  * When likes are depleted:

        {
            'match': BOOL,
            'likes_remaining': 0,
            'rate_limited_until': MICROSOFT_DATE_FORMAT
        }


#### `swipe_left(user_id)`
  * GET /pass/{user_id}
  * Passes the specified user.
  * Response is status code.

#### `super_like(user_id)`
  * POST /like/{user_id}/super
  * Super likes the specified user.

        {
            'match': BOOL,
            'status': 200,
            'super_likes': {
                'remaining': NUM,
                'alc_remaining': NUM,
                'new_alc_remaining': NUM,
                'allotment': NUM,
                'resets_at': 'ISO8601'
            }
        }

#### Request headers

GET
    
    {
        'X-Auth-Token': '...'
    }

POST

    {
        'X-Auth-Token': '...',
        'Content-Type': 'application/json; charset=utf-8'
    }

### Examples

Check out `swipe_right_all.py` for an example to quickly use `TinderClient`.