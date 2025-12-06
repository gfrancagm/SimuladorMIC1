from uc import UC
from datapath import Datapath
from mp import MP

if __name__ == "__main__":
    uc = UC()
    dp = Datapath()
    mp = MP()
   
    for line in mp.memoria:
        uc.executar_passo(dp, mp)
        input("")