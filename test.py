import sys
sys.path.append('./posw')
from posw.posw import *


if __name__ == '__main__':
    print('Raymond.')
    chi = verifier_init()
    G = prover_init(chi)
    challenge_gamma = verifier_challenge()
    tau = prover_challenge(chi, G, challenge_gamma)
    print(verifier_check(chi, G.node[BinaryString(0, 0)]['label'], challenge_gamma, tau))
