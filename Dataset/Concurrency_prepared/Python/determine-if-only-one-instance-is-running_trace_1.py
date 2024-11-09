import __main__, os

def isOnlyInstance():
    return os.system("(( $(ps -ef | grep python | grep '[" +
                     __main__.__file__[0] + "]" + __main__.__file__[1:] +
                     "' | wc -l) > 1 ))") != 0

if __name__ == "__main__":
    print(isOnlyInstance())