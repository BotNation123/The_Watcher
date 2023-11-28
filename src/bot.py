from decouple import config

print(config("TOKEN"))
print(config("MONGO_URL"))
