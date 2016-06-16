import re
import bs4
import datetime

from .result import *


class BurukiParser:
	_month_num = dict(янв=1, фев=2, мар=3, апр=4, май=5, мая=5, июн=6, июл=7, авг=8, сен=9, окт=10, ноя=11, дек=12)
	_date_re = re.compile(r'(?<=\s)\d{1,2}(?=\s)[\sа-я]+\d{4}', re.I)
	_price_re = re.compile(r'\d+')
	
	def __init__(self):
		pass
	
	def parse(self, mail):
		html = [load for load in mail.get_payload() if load.get_content_type() == 'text/html'][0].get_payload()
		
		soup = bs4.BeautifulSoup(html, 'html.parser')
		
		discounts = soup.select("body > table > tr > td > table > tr > td > table > tbody > tr > td > table > tr > td > table")
		
		for discount in discounts:
			if len(discount.select("> tr > td > table > tr")[1].select("td > table")) == 0:
				continue
			
			logo = discount.select("> tr > td > table img")
			
			try:
				company = logo[0]['alt']
			except IndexError as er:
				print(discount.select("> tr"))
				raise er
				
			sale_date_text = discount.select("> tr > td > table > tr")[0].select("> td > table > tbody > tr")[-3].td.string
			flight_date_text = discount.select("> tr > td > table > tr")[0].select("> td > table > tbody > tr")[-2].td.string
			
			sale_date = self._date_re.findall(sale_date_text)
			flight_date = self._date_re.findall(flight_date_text)
			
			flights = discount.select("> tr > td > table > tr")[1].select("> td > table > tr")
			
			result = Discount(
				company = company.strip(),
				sale_date_from = self._parse_date(sale_date[0]),
				sale_date_to = self._parse_date(sale_date[1]),
				flight_date_from = self._parse_date(flight_date[0]),
				flight_date_to = self._parse_date(flight_date[1]),
				prices = list()
			)
			
			status = Status(Status.OK)
			
			for flight in flights:
				source, dest = flight.select("> td")[0].string.strip().split('⇄')
				price = int(''.join(self._price_re.findall(flight.select("td")[1].span.string.strip())))
				
				result.prices.append(Price(source = source.strip(), dest = dest.strip(), price = price))
			
			yield (status, result)
		
	def _parse_date(self, date_str):
		day_str, month_str, year_str = re.split(r'\s+', date_str)
		
		return datetime.date(
			day=int(day_str),
			month=self._month_num[month_str.lower()[:3]],
			year=int(year_str)
		)
