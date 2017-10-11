import hashlib
import sys


def getDecodeString(userCode, length):
    userCode += 'vol'
    result = ''
    for c in getMD5String(userCode):
        code = ord(c) % 10
        result = result + '%d' % code
    return result[0:length]


def getMD5String(key):
    return hashlib.md5(key).hexdigest()

def main():
    print getDecodeString(sys.argv[1], 8)

if __name__ == '__main__':
    main()
