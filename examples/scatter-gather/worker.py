from asynctools import ScatterGather

## Relay handler
def handler(payload):
    message = payload['message']
    if payload['user']:
        userdict = payload['user']
        print('I got "%s" from "%s"'%(message,userdict['profile']['real_name']))
    else:
        print('I got "%s"'%(message))
    return('ACK')


## Server relay instance
relay = ScatterGather()
#relay.slackbotHost = 'apsd-slackbot-01.ngid.centurylink.net'
relay.name = 'example'
relay.run(handler)

