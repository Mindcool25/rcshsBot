import urllib, requests

def normalize_key(key): # TODO: Make this more powerful
    return key.strip().lower()

def fetch_dictionary():
    url = 'https://www.techopedia.com/dictionary'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers) 
    il = list(filter(lambda s: '/definition' in s, str(urllib.request.urlopen(req).read()).split('\\n')))
    final_dict = {}
    for e in il:
        [value, key] = e.split('>', 1)
        final_dict[normalize_key(key.rstrip('</a>'))] = value.lstrip('<a href="/definition/').rstrip('"')
    return final_dict


def fetch_page(key, dict):
    url = 'https://www.techopedia.com/definition/' + dict[key]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return str(urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read())

def extract_definition(page):
    debut = fin = 0
    il = []
    for q in range(0, len(page)):
        if page[q:q+3] == "<p>":
            debut = q+3
        elif page[q:q+4] == '</p>':
            fin = q
            il.append(page[debut:fin])
            debut = fin+4
    return il



# link_dictionary = fetch_dictionary()
# print(list(link_dictionary)[len(link_dictionary) - 1])
# for e in lambda s: '<\small>' not in s, (extract_definition(fetch_page(normalize_key('Type inference '), link_dictionary))):
#     print(e)
#     print()

print(extract_definition('<p>hello, there.</p>iuhreoiuhveiurhn<p> Interesting.</p>kokok'))