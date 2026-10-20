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
    logic rst;

    logic tb_wr_valid;
    logic tb_wr_ready;
    logic [WIDTH-1:0] tb_wr_data;

    logic tb_rd_valid;
    logic tb_rd_ready;
    logic [WIDTH-1:0] tb_rd_data;

    logic wr_valid;
    logic wr_ready;
    logic [WIDTH-1:0] wr_data;

    logic rd_valid;
    logic rd_ready;
    logic [WIDTH-1:0] rd_data;

    assign tb_rd_ready = 1'b1;

    //==============================
    // u_dut
    //==============================
    fifo #(.WIDTH(WIDTH), .DEPTH(DEPTH)) u_dut
    (
        .clk(clk),
        .rst(rst),
        .wr_valid(wr_valid),
        .wr_ready(wr_ready),
        .wr_data(wr_data),
        .rd_valid(rd_valid),
        .rd_ready(rd_ready),
        .rd_data(rd_data)
    );

    //==============================
    // u_rand_stall_wr
    //==============================
    rand_stall #(.WIDTH(WIDTH)) u_rand_stall_wr
    (
        .clk(clk),
        .in_valid(tb_wr_valid),
        .in_ready(tb_wr_ready),
        .in_data(tb_wr_data),
        .out_valid(wr_valid),
        .out_ready(wr_ready),
        .out_data(wr_data)
    );

    //==============================
    // u_rand_stall_rd
    //==============================
    rand_stall #(.WIDTH(WIDTH)) u_rand_stall_rd
    (
        .clk(clk),
        .in_valid(rd_valid),
        .in_ready(rd_ready),
        .in_data(rd_data),
        .out_valid(tb_rd_valid),
        .out_ready(tb_rd_ready),
        .out_data(tb_rd_data)
    );

endmodule
