def get_name(who):
    name = []
    while len(name)!=2:
        name = input("first name followed by last name of %s, seperated by a space: " % (who))
        name = name.split()
    name = [name[0].capitalize(), name[1].capitalize()]
    return name