# Tinder API sniffed and wrapped in Python

I sniffed the private Tinder API using by using a web debugging proxy and mocking user scenarios on the app. By viewing the web traffic from my mobile device on the proxy, I was able to see both the HTTP requests and responses for any user scenario.

I wrapped the most relevant API calls in a python class `TinderClient`, which upon construction, authorizes the instance to use and make changes to your Tinder account.

## Sniffing your Facebook Token

In order to use `TinderClient`, you have to obtain a user authentication token from Tinder by providing your Facebook ID and Facebook Token.

The Facebook ID is easy enough, just click head over to [findmyfbid](http://findmyfbid.com/) and paste in your Facebook profile URL.

To get your Facebook Token for Tinder, you're going to have to use a web debugging proxy. Proxies like [Fiddler](http://www.telerik.com/fiddler) and [Charles](https://www.charlesproxy.com/) work just fine for this. Basically what you will have to do is connect your mobile device to the same network as your computer running the proxy, and modify your mobile device's connection settings to use a proxy with the IP address of your computer and the port used by the proxy. You may need to download certificates onto your mobile device to permit traffic through the proxy.

Once your mobile device is hooked up to the proxy, open up Tinder and a series of API calls will be made to the host `https://api.gotinder.com`; the first will be `POST /auth`. Look into the request body to find:

    {
        'facebook_token': facebook_token,
        'facebook_id': facebook_id,
        'locale': 'en'
    }

You will need your `facebook_token` whenever you want to initiate an instance of `TinderClient`. **Do not publicize your `facebook_token`.** With it, anyone can act as you on Tinder. If you ever release it and need to change it, the only alternative I know is to delete the app from your Facebook account (which will delete your Tinder bio/matches) and to sign up on Tinder with your Facebook account again.

On a side note, if you take a look at the response body of the `POST /auth` request, you'll see a key called `X-Auth-Token`. The value of this is needed in all other HTTP request headers to the Tinder API. This token does expire after sometime, which is why the Facebook Token is needed get another authorized instance.

