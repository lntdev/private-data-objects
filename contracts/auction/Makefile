# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PDO_HOME ?= /opt/pdo

SRCDIR?=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOTDIR := $(abspath $(SRCDIR)/../..)
EXTENSIONPATH := $(ROOTDIR)/common/build
INSTALLDIR = $(PDO_HOME)/contracts

CONTRACTS := _integer-key-auction.scm
DEBUG_CONTRACTS := $(addprefix _debug, $(CONTRACTS))
TEST_CONTRACTS = _aptest.scm
PLUGINS := integer-key-auction.py

all: $(CONTRACTS)

debug : $(DEBUG_CONTRACTS)

test : $(TESTS)
	@echo No automated tests defined

_integer-key-auction.scm : integer-key-auction.bld integer-key-auction.scm
	LD_LIBRARY_PATH=$(EXTENSIONPATH) tinyscheme -1 integer-key-auction.bld

_debug_integer-key-auction.scm : integer-key-auction.bld integer-key-auction.scm auction-test.scm
	LD_LIBRARY_PATH=$(EXTENSIONPATH) tinyscheme -1 integer-key-auction.bld debug test-auction

_aptest.scm : aptest.bld auction-protocol-test.scm ../integer-key/integer-key.scm integer-key-auction.scm
	LD_LIBRARY_PATH=$(EXTENSIONPATH) tinyscheme -1 aptest.bld debug aptest

install : $(CONTRACTS)
	@echo copy $(CONTRACTS) to $(INSTALLDIR)
	@mkdir -p $(INSTALLDIR)
	@cp $(CONTRACTS) $(INSTALLDIR)
	@cp $(PLUGINS) $(INSTALLDIR)

clean :
	rm -f $(CONTRACTS) $(DEBUGCONTRACTS)

.PHONY : all clean debug install test
