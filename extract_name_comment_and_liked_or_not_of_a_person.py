import requests
import json
import time

def search_dict(partial, key):
    """
    A handy function that searches for a specific `key` in a partial dictionary/list

    """
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:    # if key found then return the value of the key
                yield v
            else:      # value of the key may be another dictionary, search again
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list): # if the partial is a list
        for i in partial:  # every list may contain dictionary, that's whay search dict again
            for o in search_dict(i, key):
                yield o

def find_value(html, key, num_sep_chars=2, separator='"'):
    # defining the start position
    start_pos = html.find(key) + len(key) + num_sep_chars
    # defining the end position
    end_pos = html.find(separator, start_pos)

    return html[start_pos:end_pos]

from pprint import pprint

def get_comment(url):
    session = requests.Session()
    res = session.get(url)  # make the request
    # xsrf_token is the session_token extracting.........
    xsrf_token = find_value(res.text, "XSRF_TOKEN", num_sep_chars=3)
    # parse the YouTube initial data in the <script> tag
    data_str = find_value(res.text, 'window["ytInitialData"] = ', num_sep_chars=0, separator="\n").rstrip(";")
    data = json.loads(data_str) # converting to p[ython dictionary instead plain text

    # search for ctoken & continuation parameter field

    for r in search_dict(data, "itemSectionRenderer"):
        pagination_data = next(search_dict(r, "nextContinuationData"))
        if pagination_data:
            break  # if data we found break the loop
    continuation_tokens = [(pagination_data['continuation'], pagination_data['clickTrackingParams'])]

    while continuation_tokens: # keep looping until continuation token list is empty(no more comments)
         continuation , itct = continuation_tokens.pop()
         # constructing params parameter (the ones in the URl)
         params = {
            "action_get_comments": 1,
            "pbj": 1,
            "ctoken": continuation,
            "itct": itct,
         }
         # constructing POST by data, which consists of the XSRF token
         data = {
            "session_token": xsrf_token
         }
         # constructing request headers
         headers = {
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20200731.02.01"
         }

         # making the POST request to get the comments data
         response = session.post("https://www.youtube.com/comment_service_ajax", params=params, data=data, headers=headers)
         # convert to a python dictionary
         comments_data = json.loads(response.text)

         for comment in search_dict(comments_data, "commentRenderer"):
             yield {
                'author': comment.get('authorText', {}).get('simpleText', ''),
                'isLiked': comment['isLiked'],
                'comment': ''.join([c['text'] for c in comment['contentText']['runs']]),
             }

         # load continuation tokens for next comments (ctoken & itct)

         continuation_tokens = [(next_cdata['continuation'], next_cdata['clickTrackingParams']) for next_cdata in search_dict(comments_data, 'nextContinuationData')]+continuation_tokens
         # avoiding heavy loads with popular data
         time.sleep(0.1)


if __name__ == "__main__":
        url = input("Put the URL here: ")
        file_name = input("Put a file name you want to save as: ")
        with open("comments_file\{}.csv".format(file_name), "w", encoding='utf-8') as file:
                file.write("count, author, comment, isLiked?\n")
                for count, comment in enumerate(get_comment(url)):
                    com_info = dict(comment)
                    file.write(str(count)+","+com_info['author']+","+str(com_info['comment'].replace(',', ' ').replace('\n', ''))+","+str(com_info['isLiked'])+"\n")
        print("done..")
