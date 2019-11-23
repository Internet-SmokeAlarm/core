import unittest
import numpy

from dependencies.python.fmlaas.serde import serialize_numpy

class SerializeNumpyTestCase(unittest.TestCase):

    def test_serialize_numpy(self):
        json_data = {"test" : numpy.asarray([10.0, 15.9, 2222.2, 33.4442])}

        serialized_data = serialize_numpy(json_data)

        self.assertEqual(type(serialized_data["test"]), type(list()))
