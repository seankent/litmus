//==============================================
// top
//==============================================
module top
#(
    parameter WIDTH = 8,
    parameter DEPTH_LOG2 = 2
)
();
    logic wr_clk;
    logic wr_rst;

    logic wr_valid;
    logic wr_ready;
    logic [WIDTH-1:0] wr_data;

    logic rd_clk;
    logic rd_rst;

    logic rd_valid;
    logic rd_ready;
    logic [WIDTH-1:0] rd_data;

    //==============================
    // u_dut
    //==============================
    async_fifo #(.WIDTH(WIDTH), .DEPTH_LOG2(DEPTH_LOG2)) u_dut
    (
        .wr_clk(wr_clk),
        .wr_rst(wr_rst),
        .wr_valid(wr_valid),
        .wr_ready(wr_ready),
        .wr_data(wr_data),
        .rd_clk(rd_clk),
        .rd_rst(rd_rst),
        .rd_valid(rd_valid),
        .rd_ready(rd_ready),
        .rd_data(rd_data)
    );

endmodule
