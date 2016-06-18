#!/usr/bin/env python3
import os
import email
import time

import parse
import config
import storage
import fetch.pickle
import pypyodbc
#conn = pymssql.connect(host='DESKTOP-QF8UM51', user=r'DESKTOP-QF8UM51\nadym', password='123', database='aviaDb', as_dict=True)

#connection_string =r'Driver={SQL Server};Server=<DESKTOP-QF8UM51>;Database=<aviaDb>;Uid=<Admin>;Pwd=<1>;'
#connection = pypyodbc.connect(connection_string)

class DataBase:
    def __init__(self):
        self._fetcher = fetch.pickle.FetchPickle(dump_file='../../data/dump.pickle')

    def fetch(self):
        raise NotImplementedError()

    def get_cursor(self):
        connection = pypyodbc.connect(driver='{SQL Server}', server='DESKTOP-QF8UM51', database='aviaDb', uid='Admin', pwd='1')
        #SQL = 'SELECT * FROM <YOURTABLE>'
        # cur.execute(SQL)
        # cur.close()
        # connection.close()
        cur = connection.cursor()
        return cur

    def InsertData(self):
        #'INSERT INTO dbo.Race (ID, Companyid, PointBegin, PointEnd, FlyBegin, FlyEnd, FlyNotBegin, FlyNotEnd, BuyBegin, BuyEnd, Price, Link)
                               # values ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})'
                               # .format(num + 1, result.company, x.source, x.dest, result.flight_date_from, result.flight_date_to, Null, Null, result.sale_date_from, result.sale_date_to, x.price, Null)

        mails = self._fetcher.fetch_all()

        for num, mail in enumerate(mails):
            _, from_addr = email.utils.parseaddr(mail['From'])
            par = config.parser_map[from_addr]

            print('Письмо #{0} от {1}'.format(num + 1, mail['Date']))

            for status, result in par.parse(mail):
                print('\t{1}: {2} // Продажа с {3} по {4}, Полеты с {5} по {6}'.format(
                    num + 1, ['OK', 'W', '!!!'][status.status], result.company,
                    result.sale_date_from, result.sale_date_to,
                    result.flight_date_from, result.flight_date_to))

                print('\tЦены: \n',
                      ''.join(['\t\t{0} <-> {1} {2:,d} р\n'.format(x.source, x.dest, x.price) for x in result.prices]))
                print(['INSERT INTO dbo.Race (ID, Companyid, PointBegin, PointEnd, FlyBegin, FlyEnd, FlyNotBegin, FlyNotEnd, BuyBegin, BuyEnd, Price, Link) values ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11})'.format(num + 1, result.company, x.source, x.dest, result.flight_date_from, result.flight_date_to, 'Null', 'Null', result.sale_date_from, result.sale_date_to, x.price, 'Null')for x in result.prices])


            print()



main = DataBase()
main.InsertData()
'''
cur.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
for row in cur:
    print "ID=%d, Name=%s" % (row['id'], row['name'])
'''
