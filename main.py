from uc import UC
from datapath import Datapath
from memoria_principal import MP

dp = Datapath()
uc = UC()
mp = MP()

uc.run(dp, mp)
