import json
import unittest

from Yusi.YuServer.server import Status


STATUS_OK = '200 OK'
STATUS_BAD_REQUEST = '400 BAD REQUEST'


class ApplicationTest(unittest.TestCase):

  def setUp(self):
    super(ApplicationTest, self).setUp()
    from Yusi.YuServer import application
    self.application = application.application
    self.test_application = self.application.test_client()

  def AssertResultStatus(self, expected_status, res):
    if expected_status != res.status:
      print(res.data)
      self.fail()

  def testPing(self):
    res = self.test_application.get('/ping')
    self.AssertResultStatus(STATUS_OK, res)
    status = Status.FromSimple(json.loads(res.data))
    self.assertEquals(status.message, 'Yusi Server')


if __name__ == '__main__':
    unittest.main()
