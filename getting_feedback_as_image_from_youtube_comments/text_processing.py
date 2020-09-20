lst = ['a','b','c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s',
       't','u','v','w','x','y','z', ' ']

def processedText(file_name):
    with open("texts\{}.txt".format(file_name), "r", encoding="utf-8") as file:
        texts = ''.join(file.readlines())

    processed_words = ""
    for word in texts:
        if word in lst:
            processed_words += word
        else:
            continue

    return processed_words



