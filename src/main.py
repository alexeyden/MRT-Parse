#!/usr/bin/env python3

import os
import email
import time

import parser
import config
import storage
import fetch.pickle


class Main:
    def __init__(self):
        self._fetcher = fetch.pickle.FetchPickle(dump_file = '../data/dump.pickle')

    def fetch(self):
        raise NotImplementedError()

    def fetch_all(self):
        mails = self._fetcher.fetch_all()

        for num, mail in enumerate(mails):
            _, from_addr = email.utils.parseaddr(mail['From'])
            par = config.parser_map[from_addr]

            print('Письмо #{0} от {1}'.format(num + 1, mail['Date']))

            for status, result in par.parse(mail):
                print('\t{1}: {2} // Продажа с {3} по {4}, Полеты с {5} по {6}'.format(
                    num + 1, ['OK','W','!!!'][status.status], result.company,
                    result.sale_date_from, result.sale_date_to,
                    result.flight_date_from, result.flight_date_to))

                print('\tЦены: \n', ''.join(['\t\t{0} <-> {1} {2:,d} р\n'.format(x.source, x.dest, x.price) for x in result.prices]))

            print()

main = Main()
main.fetch_all()
