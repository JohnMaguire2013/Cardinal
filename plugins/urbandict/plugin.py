from urllib import urlopen
import json

from cardinal.decorators import command, help

URBANDICT_API_PREFIX = 'http://api.urbandictionary.com/v0/define?term='


class UrbanDictPlugin(object):
    @command(['ud', 'urbandict'])
    @help('Returns the top Urban Dictionary definition for a given word.')
    @help('Syntax: .ud <word>')
    def get_ud(self, cardinal, user, channel, msg):
        try:
            word = msg.split(' ', 1)[1]
        except IndexError:
            cardinal.sendMsg(channel, 'Syntax: .ud <word>')
            return

        try:
            url = URBANDICT_API_PREFIX + word
            f = urlopen(url).read()
            data = json.loads(f)

            word_def = data['list'][0]['definition']
            link = data['list'][0]['permalink']

            response = 'UD for %s: %s (%s)' % (word, word_def, link)

            cardinal.sendMsg(channel, response.encode('utf-8'))
        except Exception:
            cardinal.sendMsg(channel, "Could not retrieve definition for %s" % word)


def setup():
    return UrbanDictPlugin()
