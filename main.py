import re
import csv

from pprint import pprint

def savecsv(contacts_list):
    ''' save in phonebook.csv '''
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

def opencsv():
    ''' open phonebook_raw.csv '''
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

# def test(name):

    # title = {'lastname': None,
    #  'firstname': None,
    #  'surname': None,
    #  'organization': None,
    #  'position': None,
    #  'phone': None,
    #  'email': None}

    # fio = re.compile(r'[А-Я][а-я]+(?:\s|,)[А-Я][а-я]+(?:\s|,)(?:[А-Я][а-я]+,|,,)')
    # fio_groups = re.compile(r'([А-Я][а-я]+)(?:\s|,)([А-Я][а-я]+)(?:\s|,)(?:([А-Я][а-я]+),|,,)')
    # org_pos = re.compile(r'[^,]*,[^,]*,[^,]*,([^,]*),([^,]*),[^,]*,[^,]*')
    # tel = re.compile(r'((?:\+7|8))\s*(?:\((\d\d\d)\)|(\d\d\d))(?:-|\s?)(\d\d\d)(?:-|\s?)(\d\d)(?:-|\s?)(\d\d)(?:\s*\(*(доб\.)\s*(\d{3,5})|)')
    # email = re.compile(r',((?:\w+\.|)\w+@\w+\.\w+)')

def getphone(s):
    tel = re.compile(r'((?:\+7|8))\s*(?:\((\d\d\d)\)|(\d\d\d))(?:-|\s?)(\d\d\d)(?:-|\s?)(\d\d)(?:-|\s?)(\d\d)(?:\s*\(*(доб\.)\s*(\d{3,5})|)')
    g =  tuple(_ for _ in tel.match(s).groups() if _)
    # +7(999)999-99-99 доб.9999
    if len(g) >= 5:
        res = f'+7({g[1]}){g[2]}-{g[3]}-{g[4]}'
        if len(g) == 7:
            res = res + f' доб.{g[6]}'
    else:
        res  = len(g)
    return res


def main():
    tlist = opencsv()
    data_list = []
    phonebookadict = {}
    for index, item in enumerate(tlist):
        if index:
            data_dict = {key: value for key, value in zip(title, item)}
            names_ = ' '.join(data_dict[title[ii_]] for ii_ in range(3))
            for i_ ,n_ in enumerate(names_.split()):
                data_dict[title[i_]] = n_
            data_list.append(data_dict)
            prim_key = (data_dict[title[0]], data_dict[title[1]])
            if prim_key in phonebookadict:
                phonebookadict[prim_key] = {k: [data_dict[k], v][bool(v)] for k, v in phonebookadict[prim_key].items()}
            else:
                phonebookadict[prim_key] = data_dict
        else:
            title = item

    print(*data_list, sep='\n')
    print('---------------------------------------------------------------')
    pprint(phonebookadict, sort_dicts=False)
    print('---------------------------------------------------------------')
    contacts_list = [title]
    for value in phonebookadict.values():
        res = getphone(value['phone'])
        value['phone'] = res
        contacts_list.append([v.strip() for v in value.values()])
        print(f"--phone-{value['lastname']} {value['firstname']} {value['surname']}--------")
        print(res)
    print('---------------------------------------------------------------')
    print(*contacts_list, sep='\n')

    with open("phonebook.csv", "w", encoding='utf-8', newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

if __name__ == '__main__':
    main()