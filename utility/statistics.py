def percentage(part, whole):
    return 100 * float(part)/float(whole)


def is_growing(data):
    if percentage(data[0], data[-1]) < 100:
        return True
    return False
