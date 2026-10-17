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
    logic wr_valid;
    logic wr_ready;
    logic [WIDTH-1:0] wr_data;
    logic rd_valid;
    logic rd_ready;
    logic [WIDTH-1:0] rd_data;

    assign rd_ready = 1'b1;

    //==============================
    // dut
    //==============================
    fifo #(.WIDTH(WIDTH), .DEPTH(DEPTH)) dut
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

endmodule
