import json
import pickle
import requests

def upload(sa, data):

    API_KEY = 'key'
    NIMBITS_USER = 'aandreuisabal@gmail.com'
    NIMBITS_ADDRESS = 'http://osnimbits.appspot.com'

    '''
    # Will contain all datastreams and its values
    point = {}
    for i in range(0, len(data)):
        pass


    # Form a valid JSON dictionary
    for i in range(0, len(data)):
        try:
            feed['datastreams'] = feed['datastreams'] + (\
                    {'id': str(i),\
                    'current_value': str(data[i])\
                    }\
                    ,)
        except IndexError as e:
            print 'ERROR: ', e
            exit()


    # Write JSON object
    with open('feed.json', mode='w') as f:
        json.dump(feed, f, indent=4)
    '''


    try:
        # Try to open auxiliar file
        addr_file = open('addr.pck', 'r')
        addr = pickle.load(addr_file)

        if not addr.has_key(sa):

            # Create folder and its respective points
            addr_file.close()
            addr_file = open('addr.pck', 'w')


            # Feed metadata JSON file (a.k.a. category in Nimbits)
            feed_json = {}
            feed_json['name'] = sa
            feed_json['description'] = 'Feed for device ' + sa
            feed_json['entityType'] = 2
            feed_json['protectionLevel'] = 2
            feed_json['alertType'] = 0
            feed_json['parent'] = NIMBITS_USER
            feed_json['owner'] = NIMBITS_USER

            # Feed dict that makes the petition
            feed = {}
            feed['email'] = NIMBITS_USER
            feed['key'] = API_KEY
            feed['action'] = 'createmissing'
            feed['type'] = 'category'
            feed['json'] = str(feed_json)

            r = requests.post(NIMBITS_ADDRESS + '/service/v2/entity', params=feed)
            print r

            ### Pt. II

            # List that contains every JSON file that defines a single point
            points_json = []

            for i in range(0, len(data)):
                points_json.append({})
                points_json[i]['name'] = str(i)
                points_json[i]['description'] = 'Feed number ' + str(i)
                points_json[i]['entityType'] = 1
                points_json[i]['protectionLevel'] = 2
                points_json[i]['alertType'] = 0
                points_json[i]['value'] = data[i]
                #points_json[i]['parent'] = '12f78d0e-a218-44a5-835d-3e9df2e21b14'
                points_json[i]['key'] = NIMBITS_USER
                points_json[i]['owner'] = NIMBITS_USER

                point = {}
                point['email'] = NIMBITS_USER
                point['key'] = API_KEY
                point['action'] = 'createmissing'
                point['type'] = 'point'
                point['json'] = str(points_json[i])

                print "#################################################"
                q = requests.post('http://cloud.nimbits.com/service/v2/entity', params=point)
                print "#################################################"
            #print q.url
            #print 'Point creation: ', str(q)

            # If the packet is successfully received, save
            # the address in 'addr_file'
            if '200' in str(r):
                addr[sa] = sa

            pickle.dump(addr, addr_file)

        else:
            # use requests library to post to nimbits
            #r = requests.post("http://osnimbits.appspot.com/service/currentvalue", data=data)
            #print out[1]
            pass


    except EOFError:
        addr_file = open('addr.pck', 'w')
        pickle.dump({}, addr_file)
    except IOError:
        print 'WARNING: There is no addresses file, creating a new one...'
        addr_file = open('addr.pck', 'w')
        pickle.dump({}, addr_file)
    finally:
        addr_file.close()


    # use requests library to post to nimbits
    #r = requests.post("http://osnimbits.appspot.com/service/currentvalue", data=data)
