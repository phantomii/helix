# Copyright 1999-2016 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

EAPI=6
PYTHON_COMPAT=( python2_7 )
PYTHON_REQ_USE="threads(+)"

inherit distutils-r1

DESCRIPTION="Trading platform"
HOMEPAGE="https://helix.synapse.net.ru/"
SRC_URI=""
LICENSE="Apache-2.0"
KEYWORDS="~amd64 ~arm ~ia64 ~x86"
SLOT="0"

IUSE="test mysql"

DEPEND="
	dev-python/setuptools[${PYTHON_USEDEP}]
	>=dev-python/pbr-1.8.0[${PYTHON_USEDEP}]
	>=dev-python/six-1.7.0[${PYTHON_USEDEP}]
	>=dev-python/oslo-config-1.9.0[${PYTHON_USEDEP}]
	>=dev-python/pyyaml-3.11[${PYTHON_USEDEP}]
	>=dev-python/sqlalchemy-1.0.12[${PYTHON_USEDEP}]
	test? (
		>=dev-python/coverage-3.6[${PYTHON_USEDEP}]
		>=dev-python/mock-1.0.1[${PYTHON_USEDEP}]
		>=dev-python/nose-1.3.0[${PYTHON_USEDEP}]
		>=dev-python/hacking-0.10.1[${PYTHON_USEDEP}]
		>=dev-python/testtools-1.5.0[${PYTHON_USEDEP}]
		dev-vcs/git
	)"
PDEPEND="dev-python/pip[${PYTHON_USEDEP}]"