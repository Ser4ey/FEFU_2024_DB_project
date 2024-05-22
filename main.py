from repository import InsectDAO, SquadDAO, FamilyDAO

if __name__ == "__main__":
    # a = InsectDAO()
    #
    # print(a.select_all())
    #
    # print(a.count())

    s = SquadDAO()
    # s.add_squad("sd")
    # s.add_squad("sd2")
    # s.add_squad("sd2")

    print(s.select_all())

    f = FamilyDAO()

    f.add_squad("TEST F23", 2)

    print(f.select_all())


