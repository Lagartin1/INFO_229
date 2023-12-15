from tablero import Tablero

def main() -> None:
    print("\nBienvenido al Juego de Buscaminas de INFO229!!\n")
    tablero = Tablero()  # Instancia del tablero singleton
    tablero.jugar()      # Inicia la partida

if __name__ == "__main__":
    main()
