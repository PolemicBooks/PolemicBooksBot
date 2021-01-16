import unicodedata


# Este método é usado para remover os acentos de uma string.
def remove_accents(string: str) -> str:
	
    nfkd = unicodedata.normalize('NFKD', string)
    
    return "".join(
		[
			character for character in nfkd if not unicodedata.combining(character)
		]
	)
