#!/ usr/bin /env python3
import sys

def main () :
 for line in sys . stdin :
line = line . rstrip ("\n") # lire une ligne
 for word in line . split () : # Decoupage de la ligne par
espaces / blancs
 emit ( word , 1) # Emet (mot , 1)
9
10 def emit ( key , value ) : # Emet des paires (cle , valeur )
11 print ( f"{key }\t{ value }")
12
13 if __name__ == " __main__ ":
14 main ()
