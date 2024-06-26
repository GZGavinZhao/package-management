# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, Solus Project
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Metadata module provides access to metadata.xml. metadata.xml is
generated during the build process of a package and used in the
installation. Package repository also uses metadata.xml for building
a package index.
"""

from pisi import translate as _

import pisi.specfile as specfile
import pisi.pxml.xmlfile as xmlfile
import pisi.pxml.autoxml as autoxml
import pisi.util as util


class Delta(metaclass=autoxml.autoxml):
    t_PackageURI = [autoxml.String, autoxml.OPTIONAL]
    t_PackageSize = [autoxml.Long, autoxml.OPTIONAL]
    t_PackageHash = [autoxml.String, autoxml.OPTIONAL, "SHA1Sum"]
    a_buildFrom = [autoxml.String, autoxml.OPTIONAL]
    a_releaseFrom = [autoxml.String, autoxml.OPTIONAL]


class Source(metaclass=autoxml.autoxml):
    t_Name = [autoxml.String, autoxml.MANDATORY]
    t_Homepage = [autoxml.String, autoxml.OPTIONAL]
    t_Packager = [specfile.Packager, autoxml.MANDATORY]


class Package(specfile.Package, xmlfile.XmlFile, metaclass=autoxml.autoxml):
    t_Build = [autoxml.Integer, autoxml.OPTIONAL]
    t_BuildHost = [autoxml.String, autoxml.OPTIONAL]
    t_Distribution = [autoxml.String, autoxml.MANDATORY]
    t_DistributionRelease = [autoxml.String, autoxml.MANDATORY]
    t_Architecture = [autoxml.String, autoxml.MANDATORY]
    t_InstalledSize = [autoxml.Long, autoxml.MANDATORY]
    t_PackageSize = [autoxml.Long, autoxml.OPTIONAL]
    t_PackageHash = [autoxml.String, autoxml.OPTIONAL, "SHA1Sum"]
    t_PackageURI = [autoxml.String, autoxml.OPTIONAL]
    t_DeltaPackages = [[Delta], autoxml.OPTIONAL]
    t_PackageFormat = [autoxml.String, autoxml.OPTIONAL]

    t_Source = [Source, autoxml.OPTIONAL]

    def get_delta(self, release):
        for delta in self.deltaPackages:
            if delta.releaseFrom == str(release):
                return delta
        else:
            return None

    def decode_hook(self, node, errs, where):
        self.version = self.history[0].version
        self.release = self.history[0].release

    def __str__(self):
        s = specfile.Package.__str__(self)
        i_size = util.human_readable_size(self.installedSize)
        size = "%.2f %s" % (i_size[0], i_size[1])

        s += _("Distribution: %s, Dist. Release: %s\n") % (
            self.distribution,
            self.distributionRelease,
        )
        s += _("Architecture: %s, Installed Size: %s") % (self.architecture, size)

        if self.packageSize:
            p_size = util.human_readable_size(self.packageSize)
            size = "%.2f %s" % (p_size[0], p_size[1])
            s += _(", Package Size: %s") % size

        return s


class MetaData(xmlfile.XmlFile, metaclass=autoxml.autoxml):
    """Package metadata. Metadata is composed of Specfile and various
    other information. A metadata has two parts, Source and Package."""

    tag = "PISI"

    t_Source = [Source, autoxml.MANDATORY]
    t_Package = [Package, autoxml.MANDATORY]
    # t_History = [ [Update], autoxml.mandatory]

    def from_spec(self, src, pkg, history):
        # this just copies fields, it doesn't fix every necessary field
        self.source.name = src.name
        self.source.homepage = src.homepage
        self.source.packager = src.packager
        self.package.source = (
            self.source
        )  # FIXME: I know that replication sucks here, but this is the easiest for now-- exa
        self.package.name = pkg.name
        self.package.summary = pkg.summary
        self.package.description = pkg.description
        self.package.icon = pkg.icon
        # merge pkg.isA with src.isA
        pkg.isA.extend(src.isA)
        self.package.isA = pkg.isA
        self.package.partOf = pkg.partOf
        self.package.license = pkg.license
        self.package.packageDependencies = pkg.packageDependencies
        self.package.packageAnyDependencies = pkg.packageAnyDependencies
        self.package.componentDependencies = pkg.componentDependencies
        self.package.files = pkg.files
        # FIXME: no need to copy full history with comments
        self.package.history = history
        self.package.conflicts = pkg.conflicts
        self.package.replaces = pkg.replaces
        self.package.providesComar = pkg.providesComar
        self.package.providesPkgConfig = pkg.providesPkgConfig
        self.package.providesPkgConfig32 = pkg.providesPkgConfig32
        # self.package.requiresComar = pkg.requiresComar
        self.package.additionalFiles = pkg.additionalFiles

        # FIXME: right way to do it?
        self.source.version = src.version
        self.source.release = src.release
        self.package.version = src.version
        self.package.release = src.release
