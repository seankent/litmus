//==============================================
// top
//==============================================
module top
#(
    parameter WIDTH = 8,
    parameter DEPTH = 4
)
();

logic clk;
logic valid;
logic we;
logic [$clog2(DEPTH)-1:0] addr;
logic [WIDTH-1:0] wr_data;
logic [WIDTH-1:0] rd_data;

//==============================
// dut
//==============================
ram #(.WIDTH(WIDTH), .DEPTH(DEPTH)) dut
(
    .clk(clk),
    .valid(valid),
    .we(we),
    .addr(addr),
    .wr_data(wr_data),
    .rd_data(rd_data)
);

endmodule
