#!/usr/bin/env python3
import argparse
import os
import email
import time

import parse
import config
import storage
import fetch.gmail


class Main:
    def __init__(self, debug=False):
        self._debug = debug
        self._fetcher = fetch.gmail.FetchGmail()

    def run(self, all_=False):
        for address in config.parser_map.keys():
            mails = (self._fetcher.fetch_all if all_ else self._fetcher.fetch)(address)

            # TODO: ВСТАВИТЬ РАБОТУ С БД СЮДА

            if self._debug:
                self._debug_print(mails)

    def _debug_print(self, mails):
        for num, mail in enumerate(mails):
            _, from_addr = email.utils.parseaddr(mail['From'])
            par = config.parser_map[from_addr]

            print('Письмо #{0} от {1}'.format(num + 1, mail['Date']))

            for status, result in par.parse(mail):
                print('\t{1}: {2} // Продажа с {3} по {4}, Полеты с {5} по {6}'.format(
                    num + 1, ['OK', 'W', '!!!'][status.status], result.company,
                    result.sale_date_from, result.sale_date_to,
                    result.flight_date_from, result.flight_date_to))

                print('\tЦены: \n', ''.join(
                    ['\t\t{0} <-> {1} {2:,d} р\n'.format(x.source, x.dest, x.price) for x in result.prices]
                ))

            print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ну просто охренительный парсер писем.')
    parser.add_argument('-v', action='store_true', help='Вывод отладочной информации.')
    parser.add_argument('-a', action='store_true', help='Забрать все письма, включая прочитанные.')
    args = parser.parse_args()

    main = Main(debug=args.v)
    main.run(all_=args.a)
