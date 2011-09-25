import string
from random import Random

rand = Random()
RAND_SEARCH_SPACE = string.letters+string.digits
DEFAULT_FUNC = lambda word : "".join([rand.choice(RAND_SEARCH_SPACE) for letter in word])
REPEAT = 50

class Mongfuscate:
    def __init__(self, collection, function=DEFAULT_FUNC, repeat = REPEAT):
        self.collection = collection
        self.collection.ensure_index([("secret",1),("unsecret",1)],unique=True)

        self.function = function
        self.repeat = repeat

    def obfuscate(self, secret):
        #ensure secret is a string
        unsecret = self.__get_unsecret(secret)

        attempts = 0;
        success = unsecret != None
        while (attempts < self.repeat and success == False):
            unsecret = self.function(secret)
            success = self.collection.find_one({"unsecret":unsecret}) == None

            if success:
                self.collection.insert({"secret":secret,"unsecret":unsecret}, safe=True)

            attempts += 1
        if success:
            return unsecret
        else:
            return None

    def clarify(self, unsecret):
        secret = self.collection.find_one({"unsecret":unsecret},{"secret":1})
        if secret != None and "secret" in secret:
            return secret["secret"]
        else:
            return None

    def forget(self, secret, unsecret):
        if self.collection.remove({"secret":secret,"unsecret":unsecret},safe=True)["n"] > 0:
            return True
        else:
            return False

    def obliterate(self):
        """
        Forgets all of your obfuscate pairs.

        Really all of it.  Probably should not be exposed to end-users.
        Returns True if it removes data.
        Returns False otherwise.
        Mostly used for testing.
        Will throw an OperationError if it runs into network issues.
        """
        if self.collection.remove(safe=True)["n"] > 0:
            return True
        else:
            return False

    def __get_unsecret(self, secret):
        temp = self.collection.find_one({"secret":secret},{"unsecret":1})
#        temp = self.collection.find_one()
        if temp != None and "unsecret" in temp:
            return temp["unsecret"]
        else:
            return None

