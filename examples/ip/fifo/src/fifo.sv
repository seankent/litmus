//==============================================
// fifo
//==============================================
module fifo
#(
    parameter WIDTH = 1,
    parameter DEPTH = 1
)
(
    input clk,
    input rst,
    input wr_valid,
    output logic wr_ready,
    input [WIDTH-1:0] wr_data,
    output logic rd_valid,
    input rd_ready,
    output logic [WIDTH-1:0] rd_data
);

    logic we;
    logic re;

    logic [$clog2(DEPTH+1)-1:0] wr_ptr;
    logic [$clog2(DEPTH+1)-1:0] wr_ptr_nxt;
    logic wr_ptr_en;

    logic [$clog2(DEPTH+1)-1:0] rd_ptr;
    logic [$clog2(DEPTH+1)-1:0] rd_ptr_nxt;
    logic rd_ptr_en;

    assign wr_ready = (rd_ptr == 0) ? (wr_ptr != DEPTH) : (wr_ptr != (rd_ptr - 1));
    assign we = wr_valid & wr_ready;

    assign rd_valid = (rd_ptr != wr_ptr);
    assign re = 1'b1;

    assign rd_ptr_nxt = (rd_ptr == DEPTH) ? 0 : rd_ptr + 1;
    assign rd_ptr_en = rd_valid & rd_ready;

    assign wr_ptr_nxt = (wr_ptr == DEPTH) ? 0 : wr_ptr + 1;
    assign wr_ptr_en = we;

    //==============================
    // u_sdp_ram
    //==============================
    sdp_ram #(.WIDTH(WIDTH), .DEPTH(DEPTH+1)) u_sdp_ram
    (
        .clk(clk),
        .we(we),
        .wr_addr(wr_ptr),
        .wr_data(wr_data),
        .re(re),
        .rd_addr(rd_ptr),
        .rd_data(rd_data)
    );

    //==============================
    // u_d_ff_rd_ptr
    //==============================
    d_ff #(.WIDTH($clog2(DEPTH+1)), .RESET_VALUE(0)) u_d_ff_rd_ptr
    (
        .clk(clk),
        .rst(rst),
        .en(rd_ptr_en),
        .d(rd_ptr_nxt),
        .q(rd_ptr)
    );

    //==============================
    // u_d_ff_wr_ptr
    //==============================
    d_ff #(.WIDTH($clog2(DEPTH+1)), .RESET_VALUE(0)) u_d_ff_wr_ptr
    (
        .clk(clk),
        .rst(rst),
        .en(wr_ptr_en),
        .d(wr_ptr_nxt),
        .q(wr_ptr)
    );

endmodule
