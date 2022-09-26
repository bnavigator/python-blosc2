########################################################################
#
#       Created: Sep 26, 2022
#       Author:  The Blosc development team - blosc@blosc.org
#
########################################################################


"""
Small benchmark that exercises packaging of arrays larger than 2 GB.
"""

import sys
import time
import numpy as np
import blosc2


NREP = 1
N = int(4e8)  # larger than 2 GB
Nexp = np.log10(N)

store = False
if len(sys.argv) > 1:
    store = True

#blosc2.set_nthreads(2)

print("Creating NumPy array with 10**%d int64 elements:" % Nexp)
in_ = np.arange(N, dtype=np.int64)

if store:
    codec = blosc2.Codec.BLOSCLZ
    print(f"Storing with codec {codec}")
    cparams = {"codec": codec, "clevel": 9}

    c = None
    ctic = time.time()
    for i in range(NREP):
        c = blosc2.pack_array2(in_, cparams=cparams)
    ctoc = time.time()
    tc = (ctoc - ctic) / NREP
    print(
        "  Time for pack_array2:   %.3f (%.2f GB/s)) "
        % (tc, ((N * 8 / tc) / 2 ** 30)),
    )
    print("\tcr: %5.1fx" % (in_.size * in_.dtype.itemsize * 1.0 / len(c)))

    with open("pack_compress2.bl2", 'wb') as f:
        f.write(c)

else:
    with open("pack_compress2.bl2", 'rb') as f:
        c = f.read()

    out = None
    dtic = time.time()
    for i in range(NREP):
        out = blosc2.unpack_array2(c)
    dtoc = time.time()

    td = (dtoc - dtic) / NREP
    print(
        "  Time for unpack_array2:   %.3f s (%.2f GB/s)) "
        % (td, ((N * 8 / td) / 2 ** 30)),
    )
    assert np.array_equal(in_, out)