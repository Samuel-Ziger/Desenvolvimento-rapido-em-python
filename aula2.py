""" numero = {0, 1 , 'a', 'a'}
 numero.add('b')
 for i in numero:
	print(i)

aluno = {"nome" : "Ziger" , "sexo": "M", "Idade":22}

for s ,z in aluno.items():
	print(s, "-",z)
def operacao(x,y, op):
	if op == "+":
		return x + y
	elif op == '-':
		return x - y
	elif op =='x':
		return x * y
	elif op == '/':
		return x / y
print(operacao(1,4, '-'))

"""

def pesquise(lista: list , valor: int) -> None:
	for x, e in enumerate(lista):
		if e == valor:
			return x
	return None

valores = [13, 17, 19, 23]
print (pesquise(valores, 19))
print (pesquise(valores, 31))
