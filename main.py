from repository import InsectDAO

if __name__ == "__main__":
    a = InsectDAO()

    print(a.select_all())

    print(a.count())



