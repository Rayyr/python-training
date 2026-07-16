import sys  # for cl args


def getProfileCard():
    scriptName = sys.argv[0]
    username = sys.argv[1]
    age = sys.argv[2]
    city = sys.argv[3]

    print("Profile card information:\n")
    print("Username: " + username)
    print("Age: " + age)
    print("City: " + city)
    print("Script name:" + scriptName)


getProfileCard()
