from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")


mydatabase = client["instadb"]


mycollection = mydatabase["users"]


#user = {"name": "pavan verma", "email": "p@gmail.com"}
#mycollection.insert_one(user)
# Update email
mycollection.update_many(
    {"email": "pawan@gmail.com"},               # filter
    {"$set": {"email": "p@gmail.com"}}  # correct $set syntax
)

# Fetch updated document
data = mycollection.find_one({"email": "pawan@gmail.com"})
print(data)


data = mycollection.find()
for i in data:
    print(i)
mycollection.delete_one({"email":"pavan.sharma@gmail.com"})
print("User inserted successfully ✅")
