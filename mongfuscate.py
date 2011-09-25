'''
Obfuscates sensitive data with pymongo

Takes data that is too sensitive to touch for long (Social Security Number, Credit Card Number, Full Name, etc) and obfuscates it to a unique identifier, specified by the user.
'''
import string
from random import Random

rand = Random()
RAND_SEARCH_SPACE = string.letters+string.digits
DEFAULT_FUNC = lambda word : "".join([rand.choice(RAND_SEARCH_SPACE) for letter in word])
REPEAT = 50

class Mongfuscate:
    """
    The object you need to instantiate to use Mongfuscate.

    You should only need one per type of obfuscation.  If you want to obfuscate two types of data differently, it would make sense for you to make two instances.
    """


    def __init__(self, collection, function=DEFAULT_FUNC, repeat = REPEAT):
        """
        Makes an instance of Mongfuscate

        collection should be a pymongo collection
        function should be a lambda that expects the type of input you pass in and returns a basic, non-deterministic output so that collisions are random instead of deterministic.  The default function takes a string and replaces every character with a random letter or digit, but anything that doesn't use non-standard objects will work.
        repeat should be an integer, and specifies the number of times it should keep running the function to try to avoid a collision. The default is 50.
        """
        self.collection = collection
        self.collection.ensure_index([("secret",1),("unsecret",1)],unique=True)

        self.function = function
        self.repeat = repeat

    def obfuscate(self, secret):
        """
        Obfuscates the secret, and saves the secret, obfuscated pair in the collection

        If secret has not been seen before, and the obfuscated version is uniquely generated successfully, returns the obfuscated version.  If the secret has been seen before, returns the obfuscated version that was previously used.  If the obfuscated version has been seen before, tries to create new obfuscated versions until it successfully creates a unique one.  If it cannot, it returns None.  May throw a pymongo OperationError
        """
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
        """
        Takes the obfuscated version of a secret and returns the raw secret.

        If it does not recognize the obfuscated version, it will return None
        """
        secret = self.collection.find_one({"unsecret":unsecret},{"secret":1})
        if secret != None and "secret" in secret:
            return secret["secret"]
        else:
            return None

    def forget(self, secret, unsecret):
        """
        Forgets the specified secret, obfuscated secret pair.

        If the secret, unsecret pair didn't aready exist, returns False. Otherwise, on success, returns True. May throw a pymongo OperationError
        """
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
        """
        Fetches the obfuscated version of a secret if it has already been put into the collection

        If it does not exist in the collection, returns None
        """
        temp = self.collection.find_one({"secret":secret},{"unsecret":1})
        if temp != None and "unsecret" in temp:
            return temp["unsecret"]
        else:
            return None

