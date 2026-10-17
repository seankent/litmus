ifndef FIFO_DEPS
FIFO_DEPS := 1

include $(LITMUS_ROOT)/examples/ip/d_ff/deps.mk
include $(LITMUS_ROOT)/examples/ip/sdp_ram/deps.mk

VERILOG_SOURCES += $(LITMUS_ROOT)/examples/ip/fifo/src/fifo.sv
endif
