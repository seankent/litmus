//==============================================
// top
//==============================================
module top
#(
    parameter N = 4
)
();

logic clk;
logic [N-1:0] req;
logic [N-1:0] gnt;

initial clk = 1'b0;

//==============================
// dut
//==============================
arbiter #(.N(N)) dut
(
    .req(req),
    .gnt(gnt)
);

endmodule
