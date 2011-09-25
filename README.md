#Mongfuscate

##Premise
Takes sensitive information, stores it, and returns an obfuscated, unique identifier.  
Inspired by [Stripe](https://github.com/stripe)

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