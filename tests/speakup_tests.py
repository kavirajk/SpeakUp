from nose.tools import *
from tools import *
from bin.speakup import *

def test_index():
    resp=app.request("/")
    assert_response(resp)
