class EntriesSpider(object):

    def __init__(self, url):
        self.url = url
        self.dirs = []
        self.files = []
        self.users = []

    def parse(self, entries, parentdir):
        patternf = re.compile('(\w+\.\w+)\nfile')
        patternd = re.compile('(\w+)\ndir')
        patternu = re.compile('(\w+)\ndir')
        dirs = [parentdir + '/' + x for x in patternd.findall(entries)]
        files = [parentdir + '/' + x for x in patternf.findall(entries)]
        return dirs, files

    def run(self, ):
        entries = '/.svn/entries'
        actualpath = '/'
        url = self.url
        dirs = self.dirs
        dirs.append(actualpath)        
        l = len(dirs)
        i = 0
        while i < l:
            dir = dirs[i]
            uri = url + dir + entries
            i += 1
            print uri
            try:
                page = urllib2.urlopen(uri)
                d, f = self.parse(page.read(), dir)
                self.files.extend(f)
                if len(d) > 0:
                    self.dirs.extend(d)
                    l = len(dirs)
                    print l, i
            except urllib2.HTTPError as e:
                print e.reason
        return self.dirs, self.files


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        #si no usa proxy sacar estas 3 lineas
        proxy_handler = urllib2.ProxyHandler({'http': 'http://proxy:3128/'})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        
        if not url.startswith('http://') or not url.startswith('https://'):
            url = 'http://' + url
            s = EntriesSpider(url)
            d, f = s.run()
            for x in f:
                print url + x
    else:
        print 'falto la url'
    
if __name__ == "__main__":
    main()
