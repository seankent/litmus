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
    logic we;
    logic [$clog2(DEPTH)-1:0] wr_addr;
    logic [WIDTH-1:0] wr_data;
    logic re;
    logic [$clog2(DEPTH)-1:0] rd_addr;
    logic [WIDTH-1:0] rd_data;

    //==============================
    // dut
    //==============================
    sdp_ram #(.WIDTH(WIDTH), .DEPTH(DEPTH)) dut
    (
        .clk(clk),
        .we(we),
        .wr_addr(wr_addr),
        .wr_data(wr_data),
        .re(re),
        .rd_addr(rd_addr),
        .rd_data(rd_data)
    );

endmodule
