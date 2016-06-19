#!/usr/bin/env python3
import os
import email
import time

import parse
import config
import storage
import fetch.pickle
import pypyodbc

class DataBase:
    def __init__(self):
        self._fetcher = fetch.pickle.FetchPickle(dump_file='../../data/dump.pickle')

    def fetch(self):
        raise NotImplementedError()

    def get_cursor(self, ServName, DbName, UsrName, Pwd):
        connection_string = "Driver=SQL Server;Server={0};Database={1};Uid={2};Pwd={3};".format(ServName, DbName, UsrName, Pwd)
        print("Connecting: " + connection_string)
        connection = pypyodbc.connect(connection_string)
        cursor = connection.cursor()
        print('Connected')
        return cursor

    def InsertData(self):
        #'INSERT INTO dbo.Race (ID, Companyid, PointBegin, PointEnd, FlyBegin, FlyEnd, FlyNotBegin, FlyNotEnd, BuyBegin, BuyEnd, Price, Link)
                               # values ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})'
                               # .format(num + 1, result.company, x.source, x.dest, result.flight_date_from, result.flight_date_to, Null, Null, result.sale_date_from, result.sale_date_to, x.price, Null)

        mails = self._fetcher.fetch_all()
        InsertArr = []
        for num, mail in enumerate(mails):
            _, from_addr = email.utils.parseaddr(mail['From'])
            par = config.parser_map[from_addr]

            #print('Письмо #{0} от {1}'.format(num + 1, mail['Date']))

            for status, result in par.parse(mail):
                '''
                print('\t{1}: {2} // Продажа с {3} по {4}, Полеты с {5} по {6}'.format(
                    num + 1, ['OK', 'W', '!!!'][status.status], result.company,
                    result.sale_date_from, result.sale_date_to,
                    result.flight_date_from, result.flight_date_to))

                print('\tЦены: \n',
                      ''.join(['\t\t{0} <-> {1} {2:,d} р\n'.format(x.source, x.dest, x.price) for x in result.prices]))

                print(["INSERT INTO dbo.Race (Companyid, PointBegin, PointEnd, FlyBegin, FlyEnd, FlyNotBegin, FlyNotEnd, BuyBegin, BuyEnd, Price, Link) values ('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})".format(result.company, x.source, x.dest, result.flight_date_from, result.flight_date_to, 'Null', 'Null', result.sale_date_from, result.sale_date_to, x.price, '')for x in result.prices])
                '''
                InsertArrPart = ["INSERT INTO dbo.Race (Companyid, PointBegin, PointEnd, FlyBegin, FlyEnd, FlyNotBegin, FlyNotEnd, BuyBegin, BuyEnd, Price, Link) values ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9}, '{10}')".format(1, x.source, x.dest, result.flight_date_from, result.flight_date_to, 'Null', 'Null', result.sale_date_from, result.sale_date_to, x.price, 'www')for x in result.prices]
                for a in InsertArrPart:
                    InsertArr.append(a)

            print()
        cursor = main.get_cursor('DESKTOP-QF8UM51', 'aviaDb', 'sa', '123') #db connect
        #cursor.execute(InsertArr[0])

        for SQL in InsertArr:
            cursor.execute(SQL)
            print('Inserted: {0}'.format(SQL))
        #cursor.commit() #!!! Uncomment for insert data
        cursor.close()




main = DataBase()
main.InsertData()
