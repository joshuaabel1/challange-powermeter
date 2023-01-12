

# 1. Genere una lista con los valores no repetidos de la lista ‘repetidos’.

repeated = [1,2,3,"1","2","3",3,4,5]
no_repeated = [x for x in set(repeated) if type(x) == int]
print(no_repeated)

# 2. Genere una lista con los valores en común entre la lista ‘r’ y ‘repetidos’

r = [1,"5",2,"3"]
common_values = list(set(r).intersection(repeated)) 

# El metodo intersection() 
# devuelve un conjunto con los elementos que están en ambos conjuntos.
print(common_values)

# 3. Transforme ‘d_str’ en un diccionario.

d_str = '{"valor":125.3,"codigo":123}'
print(eval(d_str))

# La función eval() evalúa una cadena como si fuera una expresión
# de Python y devuelve el resultado. 