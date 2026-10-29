//==============================================
// top
//==============================================
module top
#(
    parameter WIDTH = 8,
    parameter RESET_VALUE = 0
)
();

    logic clk;
    logic rst;
    logic en;
    logic [WIDTH-1:0] d;
    logic [WIDTH-1:0] q;
    
    //==============================
    // u_dut
    //==============================
    d_ff #(.WIDTH(WIDTH), .RESET_VALUE(RESET_VALUE)) u_dut
    (
        .clk(clk),
        .rst(rst),
        .en(en),
        .d(d),
        .q(q)
    );

endmodule
