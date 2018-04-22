import sys
sys.path.append('./posw')
from posw.posw import *


if __name__ == '__main__':
    print('Raymond.')
    chi = verifier_init()
    phi, phi_P = prover_init(chi)
    challenge_gamma = verifier_challenge()
    prover_challenge()
    verifier_check() 