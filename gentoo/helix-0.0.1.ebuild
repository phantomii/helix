# Copyright 1999-2016 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

EAPI=5
PYTHON_COMPAT=( python2_7 )
PYTHON_REQ_USE="threads(+)"

inherit distutils-r1

DESCRIPTION="Trading platform"
HOMEPAGE="https://helix.synapse.net.ru/"
SRC_URI="https://github.com/phantomii/helix/releases/download/${PV}/${P}.tar.gz"

LICENSE="Apache-2.0"
KEYWORDS="amd64 arm ia64 x86"
SLOT="0"

IUSE="test mysql mysql-client sqlite gui server"

RDEPEND="
        >=dev-python/alembic-0.7.7[${PYTHON_USEDEP}]
        >=dev-python/six-1.7.0[${PYTHON_USEDEP}]
        >=dev-python/oslo-config-1.9.0[${PYTHON_USEDEP}]
        >=dev-python/pyyaml-3.11[${PYTHON_USEDEP}]
        >=dev-python/sqlalchemy-0.7.10[${PYTHON_USEDEP}]
        test? (
            >=dev-python/coverage-3.6[${PYTHON_USEDEP}]
            >=dev-python/mock-1.0.1[${PYTHON_USEDEP}]
            >=dev-python/nose-1.3.0[${PYTHON_USEDEP}]
            >=dev-python/hacking-0.10.1[${PYTHON_USEDEP}]
            >=dev-python/testtools-1.5.0[${PYTHON_USEDEP}]
            dev-vcs/git
        )
        mysql? (
            dev-db/mysql

        )
        mysql-client? (
            dev-python/mysql-python[${PYTHON_USEDEP}]
        )
        sqlite? (
            dev-db/sqlite
        )
        gui? (
            >=dev-python/numpy-1.8.2[${PYTHON_USEDEP}]
            >=dev-python/pygobject-3.14.0[${PYTHON_USEDEP}]
        )
        server? (
            dev-python/restalchemy[${PYTHON_USEDEP}]
        )"

DEPEND="
    dev-python/setuptools[${PYTHON_USEDEP}]
    >=dev-python/pbr-0.8.2[${PYTHON_USEDEP}]
    ${RDEPEND}"

PDEPEND="dev-python/pip[${PYTHON_USEDEP}]"
