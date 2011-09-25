#Mongfuscate

##Premise
Takes sensitive information, stores it, and returns an obfuscated, unique identifier.  
Inspired by [Stripe](https://github.com/stripe)

##Dependencies
pymongo (just need to pass in a collection)

##Test
Assumes you have a non-password protected mongod running locally, and that your mongfuscate db's test collection is empty.

###Sample Usage
```python
from mongfuscate import Mongfuscate
from pymongo import Connection

collection = Connection().awesomedb.supercollection
obfusc = Mongfuscate(collection) #making the mongfuscate object

obf = obfusc.obfuscate("username") #now I have a sweet obfuscated version
real = obfusc.clarify(obf) #okay, done with playing with the obfuscated version, now I need the real version again

funky_obfusc = Mongfuscate(collection,lambda x : "".join([y for y in x])) #trivial example of passing in a lambda
obf = funky_obfusc.obfuscate("username") #now I have a sweet obfuscated version
real = funky_obfusc.clarify(obf) #okay, done with playing with the obfuscated version, now I need the real version again

#note: regardless of the function that is passed in, it should appear the same way to the end-user
```

##Indexing
Both the secret and the obfuscated secret are indexed upon, so it should be pretty fast.

##API

###Mongfuscate(self, collection, function = DEFAULT_FUNC, repeat = REPEAT)
Collection should be a pymongo collection, and function should take as a parameter your secret, and output a randomly generate obfuscated version of the secret. The default replaces every character in a string with a random letter or digit.  repeat is how many times it will retry regenerating the obfuscated version, because a non-unique key will generate confusion.  This makes a new instance of Mongfuscate.

###obfuscate(self, secret)
Secret will be stored in your mongodb collection, so it should be anything that I can store in a mongodb document, so an integer, float, string, list, dict, time are all good.  However, custom object will not be good.  The return value of this function is the obfuscated version of the secret.

###clarify(self, unsecret)
Looks up the secret in the collection based on the obfuscated version of the secret.  Returns None if it's not there, the secret if it is.

###forget(self, secret, unsecret)
If the collection contains a secret=secret, unsecret=unsecret pair, removes the pair from the collection and returns True. Otherwise, returns False.

###obliterate(self)
Forgets all of your user information. Really all of it. Probably should not be exposed to end-users. Mostly used for testing. Will throw an OperationError if it runs into network issues.

##QtMbAbHB (Questions that Might be Asked but Haven't Been Historically)
Q: Do you support python3?  
A: I haven't looked into it.
