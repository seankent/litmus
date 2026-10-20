ifndef ASYNC_FIFO_DEPS
ASYNC_FIFO_DEPS := 1

include $(LITMUS_ROOT)/examples/ip/d_ff/deps.mk
include $(LITMUS_ROOT)/examples/ip/sdp_ram/deps.mk
include $(LITMUS_ROOT)/examples/ip/sync/deps.mk

VERILOG_SOURCES += $(LITMUS_ROOT)/examples/ip/async_fifo/src/async_fifo.sv
endif
