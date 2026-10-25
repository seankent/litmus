#==============================================
# usage
#==============================================
# targets
#   sim: run the simulation (the default)
#   waves: open the waveform
#   clean: remove gen/
#   debug: run the simulation under gdb
#
# variables
#   WAVES=0: do not dump waves
#   LITMUS_LOG_FILE=<path>: write the log somewhere else
#==============================================

SIM ?= icarus
TOPLEVEL_LANG ?= verilog
WAVES ?= 1

SIM_BUILD = gen
COCOTB_RESULTS_FILE = $(SIM_BUILD)/results.xml

export LITMUS_LOG_FILE = $(SIM_BUILD)/log.json

TOPLEVEL = top
COCOTB_TEST_MODULES = test

include $(shell cocotb-config --makefiles)/Makefile.sim

#==============================================
# waves
#==============================================
.PHONY: waves
waves: $(SIM_BUILD)/$(TOPLEVEL).fst
	gtkwave $(SIM_BUILD)/$(TOPLEVEL).fst &

$(SIM_BUILD)/$(TOPLEVEL).fst: $(VERILOG_SOURCES) $(wildcard $(PWD)/*.py)
	-@$(MAKE) --no-print-directory sim
