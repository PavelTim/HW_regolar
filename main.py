import re
import csv

# from pprint import pprint

def savecsv(contacts_list, filename="phonebook.csv"):
    ''' save contacts_list: list in phonebook.csv '''
    with open(filename, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

def opencsv():
    ''' open phonebook_raw.csv '''
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def getfromline(line: str)-> list:
    ''''''
    fio_groups = re.compile(r'([А-Я][а-я]+)(?:\s|,{,2})([А-Я][а-я]+)(?:\s|,{,2})(?:([А-Я][а-я]+),|,)')
    org_pos = re.compile(r'[^,]*,[^,]*,[^,]*,([^,]*),([^,]*),[^,]*,[^,]*')
    tel = re.compile(r'((?:\+7|8))\s*\(?(\d\d\d)\)?(?:-|\s?)(\d\d\d)(?:-|\s?)(\d\d)(?:-|\s?)(\d\d)(?:\s*\(*(доб\.)\s*(\d{3,5})|)')
    email = re.compile(r',((?:\w+\.|)\w+@\w+\.\w+)')

    line_result = []
    line_result.extend(fio_groups.findall(line)[0])
    line_result.extend(org_pos.findall(line)[0])
    tel_phone = tel.search(line)
    if tel_phone:
        p = [''] * 7
        for i, v in enumerate(tel_phone.groups()):
            p[i] = v
        phone_string = f'+7({p[1]}){p[2]}-{p[3]}-{p[4]}' + ['', f' {p[5]}{p[6]}'][bool(p[5])]
    else:
        phone_string = ''
    line_result.append(phone_string)
    email_ = email.findall(line)
    line_result.extend([[''], email_][bool(email_)])
    return line_result

def test():
    ''' '''

    with open("phonebook_raw.csv", encoding='utf-8') as f:
        title = f.readline().strip().split(',')
        result_dict = {}
        for line in f:
            line_result = getfromline(line)
            if (line_result[0], line_result[1]) in result_dict:
                result_dict[(line_result[0], line_result[1])] = [
                    i_1 if i_1 else i_2 for i_1, i_2 in zip(result_dict[(line_result[0], line_result[1])], line_result)
                ]
            else:
                result_dict[(line_result[0], line_result[1])] = line_result

    contacts_list = [title]
    for value in result_dict.values():
        contacts_list.append(value)
    savecsv(contacts_list, filename='phonebook2.csv')

def getphonetest(s):
    tel = re.compile(r'((?:\+7|8))\s*\(?(\d\d\d)\)?(?:-|\s?)(\d\d\d)(?:-|\s?)(\d\d)(?:-|\s?)(\d\d)(?:\s*\(*(доб\.)\s*(\d{3,5})|)\)?')
    g = tuple(_ for _ in tel.match(s).groups() if _)
    # +7(999)999-99-99 доб.9999
    if len(g) >= 5:
        res = f'+7({g[1]}){g[2]}-{g[3]}-{g[4]}'
        if len(g) == 7:
            res = res + f' доб.{g[6]}'
    else:
        res = len(g)
    return res

def getphone(s):
    tel = re.compile(r'((?:\+7|8))\s*\(?(\d\d\d)\)?(?:-|\s?)(\d\d\d)(?:-|\s?)(\d\d)(?:-|\s?)(\d\d)(?:\s*\(*(доб\.)\s*(\d{3,5})|)\)?')
    # +7(999)999-99-99 доб.9999
    res = tel.sub(r'+7(\2)\3-\3-\4 \6\7', s)
    return res

def main():
    tlist = opencsv()

    phonebookadict = {}
    title = tlist.pop(0)
    for item in tlist:
        data_dict = {key: value for key, value in zip(title, item)}
        names_ = ' '.join(data_dict[title[i_]] for i_ in range(3))
        for i_, n_ in enumerate(names_.split()):
            data_dict[title[i_]] = n_

        prim_key = (data_dict[title[0]], data_dict[title[1]])
        if prim_key in phonebookadict:
            phonebookadict[prim_key] = {k: [data_dict[k], v][bool(v)] for k, v in phonebookadict[prim_key].items()}
        else:
            phonebookadict[prim_key] = data_dict

    contacts_list = [title]
    for value in phonebookadict.values():
        res = getphone(value['phone'])
        value['phone'] = res
        contacts_list.append([v.strip() for v in value.values()])

    savecsv(contacts_list)

if __name__ == '__main__':
    main()
    test()