import random
import os
import time


class Casilla:
    def __init__(self, es_mina=False):
        self.es_mina = es_mina
        self.revelada = False
        
        
## Patron de diseño singleton para protejer el tablero de dos instancias en un mismo game
class Tablero:
    _instance = None
    def __new__(cls):  #constructor que setea el tamño del tablero y cuantas minas hay 
        if not cls._instance :
            nivel = ""
            while True:
                try: 
                    selecccion = (input("Nivel principiante(p)  intermedio(m)  experto(e)\nIngrese caracter: "))
                    if selecccion == "p" or selecccion == "m" or selecccion == "e":
                        nivel += selecccion
                        break
                    EOFError
                except (ValueError):
                    print("Error Valor no valido, Ingrese nuevamente")
                except TypeError:
                    print("Error Valor no valido, Ingrese nuevamente")
            if nivel == "p":
                f,c,m = 8,8,10
            elif nivel == "m":
                f,c,m = 16,16,41
            else:
                f,c,m = 16,30,100
            cls._instance=super(Tablero, cls).__new__(cls)
            cls._instance.filas,cls._instance.columnas,cls._instance.num_minas = f,c,m 
            
            cls._instance.tablero = [[Casilla() for _ in range(c)] for _ in range(f)]
            cls._instance.colocar_minas()
            return cls._instance
        """
            Inserta minas en pociones random del tablero
        """
    def colocar_minas(self) -> None:
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if not self.tablero[fila][columna].es_mina:
                self.tablero[fila][columna].es_mina = True
                minas_colocadas += 1
        """
            Muestra el tablero y dependiendo el parametro _mostrar_minas_ revela las minas
        """
    def mostrar_tablero(self, mostrar_minas=False) -> None:
        for fila in range(self.filas):
            for columna in range(self.columnas):
                casilla = self.tablero[fila][columna]
                if casilla.revelada or mostrar_minas:
                    if casilla.es_mina:
                        print("* |", end=" ")
                    else:
                        if self.contar_minas_vecinas(fila,columna) != 0 :
                            print(f"{self.contar_minas_vecinas(fila,columna)} |", end=" ")
                        else:
                            print("- |",end=" ")
                else:
                    print("X |", end=" ")
            print()
    """"
        desisde si gasta donde revalar casillas
    """
    def revelar_casilla(self, fila, columna) -> None:
        casilla = self.tablero[fila][columna]
        if casilla.revelada:
            return
        casilla.revelada = True
        if casilla.es_mina:
            return
        minas_vecinas = self.contar_minas_vecinas(fila, columna)
        if minas_vecinas == 0:
            for f in range(fila - 1, fila + 2):
                for c in range(columna - 1, columna + 2):
                    if 0 <= f < self.filas and 0 <= c < self.columnas:
                        self.revelar_casilla(f, c)
    """"
        Cuenta las minas vecinas a las casilla
    """
    def contar_minas_vecinas(self, fila, columna) -> int:
        minas_vecinas = 0
        for f in range(fila - 1, fila + 2):
            for c in range(columna - 1, columna + 2):
                if 0 <= f < self.filas and 0 <= c < self.columnas:
                    if self.tablero[f][c].es_mina:
                        minas_vecinas += 1
        return minas_vecinas
    
    """
        Inicia la partida       
    """
    def jugar(self) -> None:
        timepoInicio = time.time()
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            self.mostrar_tablero()
            fila = 0
            columna = 0
            valid = True
            while valid:
                try:
                    fila = int(input("Fila: "))
                    columna = int(input("Columna: "))
                    valid = False
                except ValueError:
                    print("Error: Valor no válido. Ingrese nuevamente.")
                    time.sleep(2)
                except TypeError:
                    print("Error: Valor no válido. Ingrese nuevamente.")
                    time.sleep(2)
            if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                if self.tablero[fila][columna].es_mina:
                    print("¡Perdiste!\n")
                    self.mostrar_tablero(mostrar_minas=True)
                    tiempoTranscurrido = (int) (time.time() - timepoInicio)
                    print(f"\nTiempo de partida: {tiempoTranscurrido} segundos ")
                    break
                
                self.revelar_casilla(fila, columna)
                casillas_no_minadas = sum(1 for fila in self.tablero for casilla in fila if not casilla.es_mina and casilla.revelada)
                if casillas_no_minadas == (self.filas * self.columnas - self.num_minas):
                    print("¡Ganaste! \n")
                    self.mostrar_tablero(mostrar_minas=True)
                    tiempoTranscurrido =(int)(  time.time()-timepoInicio )
                    print(f"\nTiempo de partida: {tiempoTranscurrido} segundos ")
                    break
            else:
                print("Coordenadas inválidas. Inténtalo de nuevo.")
                time.sleep(2)



def main() -> None:
    print("\nBienvenido al Juego de Buscaminas de INFO229!!\n")
    tablero = Tablero()  #instacia tablero singleton
    tablero.jugar() # incia parrida

if __name__ == "__main__":
    main()
