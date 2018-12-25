#!/usr/bin/python3.6

import json

def main():
    lookup_obj = None
    with open("urls.json", "r") as f:
        lookup_obj = json.load(f);

    try:
        while True:
            query = input(" -> you@searchEngine: ").split(' ')
            res = []

            for k, v in lookup_obj.items():
                for q in query:
                    if (q in k or q.upper() in k or q.lower() in k or q[0].upper() + q[1:] in k or q in v or q.upper() in v or q.lower() in v or q[0].upper() + q[1:] in v) and not k in res:
                        
                        res.append(k)
                        print('\t~> ', k)
            if not len(res):
                print('\t~> Sorry, but no results where found.')

    except KeyboardInterrupt:
        print("\n [.] Exiting: Bye!")

if __name__ == '__main__':
    main()
