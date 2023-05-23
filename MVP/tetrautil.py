import pygit2

def getHash(self):
    try:
        repo = pygit2.Repository(self.config['World']['Directory'])
        return str(repo.revparse_single('HEAD').hex)
    except:
        return ''

def getHashUpstream(self):
    try:
        repo = pygit2.Repository(self.config['World']['Directory'])
        return str(repo.revparse_single('HEAD').hex) # For now.
    except:
        return ''
