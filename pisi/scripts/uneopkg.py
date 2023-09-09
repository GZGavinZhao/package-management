# Copyright (C) 2006-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import sys
from zipfile import BadZipfile

from pisi.package import Package


def usage(errmsg):
    print(
        """
    Error: %s

    Usage:
      uneopkg eopkg_package.eopkg [target_dir]
    """
        % (errmsg)
    )

    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage("eopkg package required..")

    elif not os.path.exists(sys.argv[1]):
        usage("File %s not found" % sys.argv[1])

    try:
        package = Package(sys.argv[1])
    except BadZipfile as e:
        print(e)
        sys.exit(1)

    if not os.path.exists("install"):
        os.makedirs("install")

    target = "." if len(sys.argv) == 2 else sys.argv[2]

    package.extract_pisi_files(target)
    package.extract_dir("comar", target)
    if not os.path.exists(os.path.join(target, "install")):
        os.makedirs(os.path.join(target, "install"))

    package.extract_install(os.path.join(target, "install"))

    # FIXME: There is a Pisi bug, it already creates an install directory even its empty.
    if os.listdir("install") == []:
        os.rmdir("install")

    return 0


if __name__ == "__main__":
    sys.exit(main())
