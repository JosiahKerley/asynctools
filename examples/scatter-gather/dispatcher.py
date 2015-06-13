from asynctools import ScatterGather

## Client
client = ScatterGather()
#relay.slackbotHost = 'apsd-slackbot-01.ngid.centurylink.net'
'''
def relayClient(msg,name,message):
    client.disatch(name,message,user=False)
    msq.reply(client.gather(name))
'''

print 'start'
client.scatter('example','this is a test',user=False)
print client.gather('example')
print client.listRelays()
print 'end'














