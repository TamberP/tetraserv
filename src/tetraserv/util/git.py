# TetraServ git integration stuff goes here.

import pygit2
import tetraserv

def getHash(self):
    if(self.flag['Git']):
        try:
            repo = pygit2.Repository(self.config['World']['directory'])
            return str(repo.revparse_single('HEAD').hex)
        except:
            return ''
    else:
        return ''

def getUpstreamHash(self):
    if(self.flag['Git']):
        try:
            repo = pygit2.Repository(self.config['World']['directory'])
            return repo.revparse_single(str(self.config['Git']['upstream'] + "/" + self.config['Git']['branch'])).hex
        except:
            return ''
    else:
        return ''
