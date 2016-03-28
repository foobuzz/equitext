"""
A text-to-text encoding. Characters in the encoded text all have the same
number of occurences. It makes the text length grow by a factor of about
1.44.
"""

import math

version = '1'


def get_combindex(chunk, tebahpla):
	"""Return the index of a combination of characters belonging to the given
		alphabet.

		:param chunk: The combination of characters, given as a string
		:param tebahpla: a dictionary containing characters of the alphabet as
			keys and their ordinal (that is, their position in the alphabet)
			as values.
	
		:returns: The index of the given combination, an integer."""
	p = len(chunk) - 1
	total = 0
	for char in chunk:
		total += tebahpla[char] * len(tebahpla)**p
		p -= 1
	return total


def get_combination(index, alphabet):
	"""Return the combination of characters having the given index according
		to the given alphabet.

		:param index: The index of the combination, given as an integer
		:param alphabet: The alphabet, given as a list of characters
	
		:returns: The combination corresponding to the index, a string."""
	chunk = ''
	quot = index
	while quot != 0:
		quot, remain = divmod(quot, len(alphabet))
		chunk = ''.join([alphabet[remain], chunk])
	return chunk


def get_permindex(permutation, alphabet):
	"""Return the index of a permutation of the alphabet.

		:param permutation: The permutation of the alphabet, given as a string
		:param alphabet: The alphabet, given as a list of characters
	
		:returns: The index of the given permutation, an integer."""
	radix = len(alphabet)-1
	index = 0
	subalphabet = alphabet.copy()
	for char in permutation:
		index += subalphabet.index(char) * math.factorial(radix)
		subalphabet.remove(char)
		radix -= 1
	return index


def get_permutation(index, alphabet):
	"""Return the permutation of the alphabet having the given index.

		:param index: The index of the permutation, given as an integer
		:param alphabet: The alphabet, given as a list of characters
	
		:returns: The permutation corresponding to the index, a string."""
	digits = convert_factorial(index)
	digits = [0]*(len(alphabet)-len(digits)) + digits
	subalphabet = alphabet.copy()
	permutation = ''
	for d in digits:
		char = subalphabet[d]
		permutation += char
		subalphabet.remove(char)
	return permutation


def convert_factorial(index):
	"""Convert a number into the factorial number system.

		:param index: The integer to convert

		:returns: The digits of the number in the factorial number system,
			given as a list of integers. The digits are given in the reverse
			positional fashion, that is, digits corresponding to the highest
			radices are given first"""
	digits = []
	quot = index
	value = 1
	while quot != 0:
		quot, remain = divmod(quot, value)
		digits.insert(0, remain)
		value += 1
	return digits


def get_alphabet_from_encoded(text):
	"""Return the alphabet of an equitext-encoded text.

		This simply returns the sorted list of characters used in the text (each
		character has a unique occurence in the list). While this is optimized
		for equitext-encoded texts, the simple :code:`sorted(list(set(text)))`
		is fine for nondescript texts

		:param text: The text from which extract the alphabet

		:returns: The alphabet used by the text, as a sorted list of characters"""
	alphabet = set()
	for char in text:
		if char in alphabet:
			break
		alphabet.add(char)
	return sorted(list(alphabet))


def get_chunk_length(alphabet):
	"""Return the length of chunks that equitext should use for texts using the
		given alphabet.

		:param alphabet: The alphabet, given as a list of characters

		:returns: The length of chunks to use with this alphabet, an integer"""
	len_chunk = 0
	while len(alphabet)**len_chunk <= math.factorial(len(alphabet)):
		len_chunk += 1
	return len_chunk - 1


def histogram(text, size=1, precision=3, occ=False, symbol='=', sort=1,
	reverse=True):
	"""Print the histogram of occurences of characters in the given text

		:param text: The text to print the histogram for
		:param size: A coefficient which impacts the width of the histogram
			proportionally to its default width which is 80-characters
		:param precision: The precision for the ratios printed at the tip of
			the histogram's bar. Must be an integer.
		:param occ: A boolean which indicates whether to display the absolute
			number of occurences of each character in addition to their ratio
		:param symbol: The string which constitutes one unit of histogram's bar
		:param sort: If set to 0, sort the histogram according to the
			chracters Unicode code points. If set to 1, sort the histogram
			according to the number of occurences of each characters
		:param reverse: Reverse the order of the sort

		:returns: None
		"""
	occurs = {}
	max_occur = 0
	for char in text:
		if char in occurs:
			occurs[char] += 1
		else:
			occurs[char] = 1
		if occurs[char] > max_occur:
			max_occur = occurs[char]

	s_occurs = sorted(list(occurs.items()), key=lambda e: e[sort],
		reverse=reverse)

	# One line is made of:
	# character + space + bar + space + frequency + (space + occ)
	# This is character + space + space + frequency = 3 + frequency:
	barless_len = 3 + len(str(round(max_occur/len(text), precision)))
	# Additional optional occurence between parenthesis:
	if occ:
		barless_len += 3 + len(str(max_occur))
	# We want the biggest line to fit in 80 characters
	unitlen = (80-barless_len)/max_occur
	# The size makes the histogram bigger or shorter:
	unitlen *= size
	
	for char, occur in s_occurs:
		line = ' '.join([
			char,
			symbol*int(unitlen*occur),
			str(round(occur/len(text), precision))
			])
		if occ:
			line += ' ({})'.format(occur)
		print(line)


def encode(text):
	"""Encode a text using equitext

		:param text: The string to encode

		:returns: The encoded string
	"""
	alphabet = sorted(list(set(text)))
	if len(alphabet) <= 1:
		return text
	tebahpla = {c:i for i, c in enumerate(alphabet)}
	len_chunk = get_chunk_length(alphabet)
	len_pad = len_chunk - len(text)%len_chunk
	text += alphabet[len_pad] * len_pad
	encoded = ''
	for i in range(0, len(text), len_chunk):
		chunk = text[i:i+len_chunk]
		index = get_combindex(chunk, tebahpla)
		encoded += get_permutation(index, alphabet)
	return encoded


def decode(text):
	"""Decode a text using equitext

		:param text: The string to decode

		:returns: The decoded string
	"""
	alphabet = get_alphabet_from_encoded(text)
	if len(alphabet) <= 1:
		return text
	len_chunk = get_chunk_length(alphabet)
	decoded = ''
	for i in range(0, len(text), len(alphabet)):
		permutation = text[i:i+len(alphabet)]
		index = get_permindex(permutation, alphabet)
		chunk = get_combination(index, alphabet)
		chunk = ''.join([alphabet[0]*(len_chunk-len(chunk)), chunk])
		decoded += chunk
	len_pad = alphabet.index(decoded[-1])
	return decoded[:-len_pad]


if __name__ == '__main__':
	histogram('hello, world!')
