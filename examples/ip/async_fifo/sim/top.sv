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

    logic tb_wr_valid;
    logic tb_wr_ready;
    logic [WIDTH-1:0] tb_wr_data;

    logic rd_clk;
    logic rd_rst;

    logic rd_valid;
    logic rd_ready;
    logic [WIDTH-1:0] rd_data;

    logic tb_rd_valid;
    logic tb_rd_ready;
    logic [WIDTH-1:0] tb_rd_data;

    assign tb_rd_ready = 1'b1;

    //==============================
    // dut
    //==============================
    async_fifo #(.WIDTH(WIDTH), .DEPTH_LOG2(DEPTH_LOG2)) dut
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

    //==============================
    // wr_rand_stall
    //==============================
    rand_stall #(.WIDTH(WIDTH)) wr_rand_stall
    (
        .clk(wr_clk),
        .in_valid(tb_wr_valid),
        .in_ready(tb_wr_ready),
        .in_data(tb_wr_data),
        .out_valid(wr_valid),
        .out_ready(wr_ready),
        .out_data(wr_data)
    );

    //==============================
    // rd_rand_stall
    //==============================
    rand_stall #(.WIDTH(WIDTH)) rd_rand_stall
    (
        .clk(rd_clk),
        .in_valid(rd_valid),
        .in_ready(rd_ready),
        .in_data(rd_data),
        .out_valid(tb_rd_valid),
        .out_ready(tb_rd_ready),
        .out_data(tb_rd_data)
    );

endmodule
