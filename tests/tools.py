from nose.tools import *
from bin.speakup import *

def assert_response(resp,contains=None,matches=None,header=None,status="200"):
    
    assert status in resp.status, "Expected %r but %r got" %(status,resp.status)
