import unittest
from pymongo import Connection
from mongfuscate import Mongfuscate


def get_collection():
    return Connection().mongfuscate.test

class TestObfuscation(unittest.TestCase):
    def setUp(self):
        obfusc.obliterate()
        func_obfusc.obliterate()
        fish_obfusc.obliterate()

    def test_default_obfuscate(self):
        unsecret = obfusc.obfuscate(secret)
        self.assertTrue(unsecret != secret)
        self.assertTrue(len(unsecret) == len(secret))

    def test_remember_obfuscate(self):
        unsecret = obfusc.obfuscate(secret)
        self.assertTrue(unsecret == obfusc.obfuscate(secret))

    def test_clarify_obfuscate(self):
        unsecret = obfusc.obfuscate(secret)
        self.assertTrue(secret == obfusc.clarify(unsecret))

    def test_forget_obfuscate(self):
        unsecret = obfusc.obfuscate(secret)
        self.assertTrue(secret == obfusc.clarify(unsecret))
        self.assertTrue(obfusc.forget(secret, unsecret))
        self.assertFalse(secret == obfusc.clarify(unsecret))
        self.assertFalse(unsecret == obfusc.obfuscate(secret))

    def test_forget_clarification(self):
        unsecret = obfusc.obfuscate(secret)
        self.assertTrue(secret == obfusc.clarify(unsecret))
        self.assertTrue(obfusc.forget(secret, unsecret))
        unsecret = obfusc.obfuscate(secret)
        self.assertTrue(secret == obfusc.clarify(unsecret))
        self.assertTrue(unsecret == obfusc.obfuscate(secret))

    def test_different_function(self):
        unsecret = func_obfusc.obfuscate(secret)
        self.assertTrue(secret == unsecret)
        self.assertTrue(secret == func_obfusc.clarify(secret))
        self.assertTrue(secret == func_obfusc.obfuscate(secret))

    def test_fish_function(self):
        unsecret = fish_obfusc.obfuscate(secret)
        self.assertTrue("fish" == unsecret)
        self.assertTrue("fish" == fish_obfusc.obfuscate(secret))
        self.assertTrue(None == fish_obfusc.obfuscate(secret * 2))

    def test_two_obfuscate(self):
        unsecret = obfusc.obfuscate(secret)
        unsecret2 = obfusc.obfuscate(secret * 2)
        self.assertTrue(secret, obfusc.clarify(unsecret))
        self.assertTrue(secret * 2, obfusc.clarify(unsecret2))


if __name__ == "__main__":
    collection= get_collection()
    obfusc = Mongfuscate(collection)
    func_obfusc = Mongfuscate(collection, lambda x : "".join([y for y in x]))
    fish_obfusc = Mongfuscate(collection, lambda x : "fish")

    secret = "secret"
    unittest.main()

