from uc import UC
from datapath import Datapath

def main():
    # 1. Instanciar os componentes
    datapath = Datapath()
    uc = UC()
    
    datapath.registrador[0] = 0

    print("Estado inicial dos registradores configurado.")
    print(f"Reg A (10): {datapath.registrador[10]}")
    print(f"Reg B (11): {datapath.registrador[11]}")

    # 3. Rodar a simulação
    # Passamos o datapath para a UC
    try:
        uc.run(datapath)
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a execução: {e}")

if __name__ == "__main__": 
    main()