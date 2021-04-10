#!/usr/bin/env python3

import sys, os, io, tempfile

from testsupport import run, subtest, info, warn


def main() -> None:

    # Get test abspath
    here = os.path.dirname(os.path.abspath(sys.argv[0]))
    with tempfile.TemporaryDirectory() as tmpdir:

        # Generate a small random file
        with open(f"{tmpdir}/rdn.txt", "wb") as fp:
            fp.write(os.urandom(4096))

        # Copy the file with the system's glibc
        with subtest("Run cp with system glibc"):
            run([ "cp", f"{tmpdir}/rdn.txt", f"{tmpdir}/rdn.glibc.txt" ])

        # Copy files with LD_PRELOADed librw.so.1
        with subtest("Run cp with librw.so.1 preloaded"):
            with open(f"{tmpdir}/stderr", "w+") as stderr:
                run([ "cp", f"{tmpdir}/rdn.txt", f"{tmpdir}/rdn.librw.1.txt" ],
                    extra_env={"LD_PRELOAD": f"{here}/../librw.so.1"},
                    stderr=stderr)
            with open(f"{tmpdir}/stderr", "r") as stderr:
                for l in stderr.readlines():
                    if "ERROR: ld.so:" in l:
                        warn(l)
                        return

        # Check that glibc and librw.so.1 give the same result
        with subtest("Check that both resulting files are identical"):
            run([ "cmp", f"{tmpdir}/rdn.glibc.txt", f"{tmpdir}/rdn.librw.1.txt" ])

    # # Check that the nbytes == 0 optimisation is implemented
    # with subtest("Check that librw.so.1 avoids the syscall if nothing will be read/written"):
    #     with open("strace.log", "r+") as fp:
    #         run([ "strace", "-o", "strace.log",
    #               "cp", "rdn.txt", "rdn.librw.1.txt" ],
    #             extra_env={"LD_PRELOAD": "librw.so.1"})

if __name__ == "__main__":
    main()