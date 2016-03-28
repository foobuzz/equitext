#! /usr/bin/env python3

import string, random, traceback, sys

import equitext


def get_random_text(max_len):
	text = ''
	for i in range(random.randrange(max_len)):
		text += random.choice(string.printable)
	return text


if __name__ == '__main__':
	texts = ['', 'a'] + [get_random_text(1000) for i in range(100)]
	for t in texts:
		try:
			t2 = equitext.decode(equitext.encode(t))
			assert t2 == t
		except:
			type_, value, tb = sys.exc_info()
			print(type_, value)
			traceback.print_tb(tb)
			print('** Text:')
			print(t)
			break
	else:
		print('OK')
