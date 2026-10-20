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
    // u_dut
    //==============================
    priority_arbiter #(.N(N)) u_dut
    (
        .req(req),
        .gnt(gnt)
    );

endmodule
