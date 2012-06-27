import urllib2
import base64
import simplejson as json
import urllib
from collections import defaultdict
from xml.etree import ElementTree

from ipdb import set_trace;
class RequestError(Exception):
    """ 
    Exception used by the API 
    """
    
    def __init__(self, errors, code='UNK.'):

        Exception.__init__(self)
        self.errors =  errors
        self.retcode = code
    def __str__(self):
        return "%s : %s" % (self.retcode, self.errors)

class FeCruServer(object):
    """ Server Fisheye & Crucible """

    @property
    def time_zone(self):
        return self._data['time_zone']

    @property
    def raw_offset(self):
        return self._data['raw_offset']

    @property
    def app_instance_dir(self):
        return self._data['app_instance_dir']

    @property
    def app_home_dir(self):
        return self._data['app_home_dir']
    
    @property
    def version(self):
        return self._data['version']
    
    @property
    def build_date(self):
        return self._data['build_date']
    
    @property
    def is_fisheye(self):
        return self._data['is_fisheye']

    @property
    def is_crucible(self):
        return self._data['is_crucible']

    def __init__(self):
        pass

    @staticmethod
    def from_xml(et):
        self = FeCruServer()
        self._data = {}
        self._data['time_zone'] = et.findtext('timeZone/ID')
        self._data['raw_offset'] = et.findtext('timeZone/rawOffset')
        self._data['app_instance_dir'] = et.findtext('appInstanceDir')
        self._data['app_home_dir'] = et.findtext('appHomeDir')
        self._data['version'] = et.findtext('version/releaseNumber')
        self._data['build_date'] = et.findtext('version/buildDate')
        self._data['is_fisheye'] = et.findtext('isFisheye')
        self._data['is_crucible'] = et.findtext('isCrucible')
        return self

    def __str__(self):
        data = ["%s:\t%s" % (attr, val) for (attr, val) in self._data.items()]
        return "[FeCruServer]\n\t" + "\n\t".join(data) + "\n[FeCruServer]" 

class Repository(object):

    def __init__(self):
        self._data = {}
        pass

    @property
    def state(self):
        return self._data.get('repositoryState')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def finished_full_slurp(self):
        return self._data.get('finishedFullSlurp')

    @property 
    def enabled(self):
        return self._data.get('enabled')

    @staticmethod
    def from_xml(et):
        self = Repository()
        for (attr, value) in et.attrib.items():
            self._data[attr] = value
        for child in et.getchildren():
            self._data[child.tag] = child.text
        return self

    def __str__(self):
        data = ["%s:\t%s" % (attr, val) for (attr, val) in self._data.items()]
        return "[Repository]\n\t" + "\n\t".join(data) + "\n[Repository]" 

class Changeset(object):

    @property
    def csid(self):
        return self._data.get('csid')

    @property
    def branches(self):
        return self._data.get('branches')

    @property
    def children(self):
        return self._data.get('children')

    @property
    def comment(self):
        return self._data.get('comment')

    @property
    def parents(self):
        return self._data.get('parents')

    @property
    def tags(self):
        return self._data.get('tags')

    @property
    def filerev(self):
        return self._data.get('fil')

    @property
    def position(self):
        return self._data.get('position')

    @property
    def display_id(self):
        return self._data.get('displayId')

    @property
    def date(self):
        return self._data.get('date')

    @property
    def branch(self):
        return self._data.get('branches')

    @property
    def children(self):
        return self._data.get('children')

    @property
    def parent(self):
        return self._data.get('parents')

    @property
    def tag(self):
        return self._data.get('tags')

    @staticmethod
    def from_xml(et):
        self = Changeset()
        self._data = {}
        if et.tag == "csid":
            self._data['csid'] = et.text
        elif et.tag == "changeset":
            self._data['branches'] = []
            self._data['children'] = []
            self._data['comment'] = ""
            self._data['parents'] = []
            self._data['tags'] = []
            self._data['filerev'] = {}
            for (attr, value) in et.attrib.items():
                self._data[attr] = value
            
            for child in et.findall('children/child'):
                self._data['children'].append(child.text)

            self._data['comment'] = unicode(et.findtext('comment'))
            
            for parent in et.findall('parent'):
                self._data['parents'].append(parent.text)

            for tag in et.findall('tag'):
                self._data['tags'].append(tag.text)

            for branch in et.findall('branch'):
                self._data['branches'].append(branch.text)
                
            for filerev in et.findall('fileRevisionKey'):
                self._data['filerev'][filerev.get('path')] = filerev.get('rev')
        return self

    def __str__(self):
        data = ["%s:%s" % (attr, repr(val)) 
                for (attr, val) in self._data.items() 
                if not attr.startswith("_")]
        return u"[Changeset: %s]\n\t" % self.csid + u"\n\t".join(data) + u"\n[Changeset]"

class Path(object):

    @property
    def name(self):
        return self._data.get('name')

    @property
    def head_deleted(self):
        return self._data.get('headDeleted')

    @property
    def is_dir(self):
        return self._data.get('dir')

    @staticmethod
    def from_xml(et):
        self = Path()
        self._data = {}
        for (attr, value) in et.attrib.items():
            self._data[attr] = value
        return self
        
    def __str__(self):
        data = ["%s:\t%s" % (attr, val) for (attr, val) in self._data.items()]
        return "[Path]\n\t" + "\n\t".join(data) + "\n[Path]" 

class RevisionInfo(object):

    @property
    def total_lines(self):
        return self._data.get('totalLines')

    @property
    def file_state(self):
        return self._data.get('fileRevisionState')

    @property
    def number(self):
        return self._data.get('rev')

    @property
    def path(self):
        return self._data.get('path')

    @property
    def lines_removed(self):
        return self._data.get('linesRemoved')

    @property
    def lines_added(self):
        return self._data.get('linesAdded')

    @property
    def date(self):
        return self._data.get('date')

    @property
    def csid(self):
        return self._data.get('csid')

    @property
    def content_link(self):
        return self._data.get('contentLink')

    @property
    def author(self):
        return self._data.get('author')

    @property
    def ancestor(self):
        return self._data.get('ancestor')

    @property
    def comment(self):
        return self._data.get('comment')

    @staticmethod
    def from_xml(et):
        self = RevisionInfo()
        self._data = {}
        for (attr, value) in et.attrib.items():
            self._data[attr] = value
        self._data['comment'] = et.findtext('comment')
        
    def __str__(self):
        data = ["%s:\t%s" % (attr, val) for (attr, val) in self._data.items()]
        return "[RevisionInfo]\n\t" + "\n\t".join(data) + "\n[RevisionInfo]" 


class API(object):
    def __init__(self, server):
        self.server = server

    @staticmethod
    def remove_query_metadata(json_decoded, result_name):
        query_metadata = {}
        for key in ['total', 'startAt', 'maxResults']:
            if key in json_decoded:
                query_metadata[key] = json_decoded.pop(key)
        return (json_decoded[result_name], query_metadata)

    def get_server(self):
        result = FeCruServer.from_xml(self.server._request_get('/rest-service-fe/server-v1'))
        return result

    def get_repos(self):
        request = self.server._request_get('/rest-service-fe/repositories-v1')
        
        result = []
        for repo in request.getchildren():
            new_repo = Repository.from_xml(repo)
            result.append(new_repo)
        return result
    
    def get_repo(self, name):
        request = self.server._request_get('/rest-service-fe/repositories-v1/%s' % name)
        new_repo = Repository.from_xml(request)
        return new_repo
    
    def get_changeset_list(self, repo_name, path=None, start=None, end=None, maxReturn=None):        
        request = self.server._request_get(
            '/rest-service-fe/revisionData-v1/changesetList/%s' % repo_name,
            path=path,
            start=start,
            end=end,
            maxReturn=maxReturn)

        result = []
        for change in request.getchildren():
            result.append(Changeset.from_xml(change))
        return result

    def get_changeset(self, repo_name, changeset_id):
        request = self.server._request_get(
            "/rest-service-fe/revisionData-v1/changeset/%s/%s" % (repo_name, changeset_id))
        return Changeset.from_xml(request)


    def get_path_list(self, repo_name, path=None):
        request = self.server._request_get(
            "/rest-service-fe/revisionData-v1/pathList/%s" % ( repo_name), path=path)
        result = []
        for path in request.getchildren():
            result.append(Path.from_xml(path))
        return result
    
    def get_revision_info(self, repo_name, path=None, revision=None):
        request = self.server._request_get(
            "/rest-service-fe/revisionData-v1/revisionInfo/%s" % repo_name, path=path, revision=revision)
        return RevisionInfo.from_xml(request)

class Server(object):
    def __init__(self, url, user, password):
        self.api = API(self)
        print "Server: %s" % url
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, user, password)
        auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)

        self.opener = urllib2.build_opener(auth_handler, urllib2.HTTPHandler(debuglevel=0))
        base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
        self.headers = {"Content-Type": "application/json", 
                        "Authorization": "Basic %s" % base64string}
        self.url = url

    def _request_get(self, url, **kwargs):
        # Filter out empty args
        args = kwargs
        for k,v in kwargs.items():
            if not v:
                del args[k]
        qs = urllib.urlencode(kwargs)
        request = urllib2.Request(self.url + url + "?" + qs, None, self.headers)
        try:
            channel = self.opener.open(request)
        except urllib2.HTTPError as response:
            raise RequestError(
                self.__decode_json_error(response.read()),
                code = 'HTTP %d' % response.code)
            
        result = channel.read()
        #print result
        return ElementTree.fromstring(result)

    def _request_post(self, url, data, **kwargs):
        qs = urllib.urlencode(kwargs)
        request = urllib2.Request(self.url + url + "?" +qs , self.__encode_json(data), self.headers)
        try:
            
            channel = self.opener.open(request)
            result = channel.read()
            if result:
                return self.__decode_json(result)

        except urllib2.HTTPError as response:
            raise RequestError(
                    response.read(), 
                code = 'HTTP %d' % response.code)
        
    def __decode_json_error(self, json_text):
        json_decoded = json.loads(json_text)
        return "[%s] %s" % (json_decoded.get('code'), json_decoded.get('message'))


if __name__ == "__main__":
    s = Server("http://localhost:3990/fecru", "admin", "admin")
    api = s.api

    print "*** SERVER ***"
    print api.get_server()
    print "*** REPOS ***"
    print api.get_repos()
    for rep in api.get_repos():
        print "*** REPO DETAIL ***"
        print api.get_repo(rep.name)
        print "*** CHANGES ****"
        for change in api.get_changeset_list(rep.name, maxReturn=1):
            print change
            print "*** CHANGE DETAIL ***"
            cset = api.get_changeset(rep.name, change.csid) 
            print cset
            try:
                print "*** REVISION INFO ***"
                print api.get_revision_info(rep.name, revision=change.csid, path='/')
            except RequestError as e:
                print  e
        
        print "*** PATHS ***"
        try:
            for path in api.get_path_list(rep.name, path='/'):
                print path
        except RequestError as e:
            print e
        
    
