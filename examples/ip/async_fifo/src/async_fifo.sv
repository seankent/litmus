//==============================================
// async_fifo
//==============================================
module async_fifo
#(
    parameter WIDTH = 1,
    parameter DEPTH_LOG2 = 2
)
(
    input wr_clk,
    input wr_rst,
    input wr_valid,
    output logic wr_ready,
    input [WIDTH-1:0] wr_data,
    input rd_clk,
    input rd_rst,
    output logic rd_valid,
    input rd_ready,
    output logic [WIDTH-1:0] rd_data
);

    localparam [DEPTH_LOG2:0] FULL_MASK = (1 << DEPTH_LOG2) | (1 << (DEPTH_LOG2-1));

    logic we;
    logic re;

    logic empty;
    logic full;

    logic [DEPTH_LOG2:0] wr_ptr;
    logic [DEPTH_LOG2:0] wr_ptr_nxt;
    logic wr_ptr_en;

    logic [DEPTH_LOG2:0] wr_ptr_gray;
    logic [DEPTH_LOG2:0] wr_ptr_gray_nxt;
    logic wr_ptr_gray_en;

    logic [DEPTH_LOG2:0] rd_ptr_gray_sync;

    logic [DEPTH_LOG2:0] rd_ptr;
    logic [DEPTH_LOG2:0] rd_ptr_nxt;
    logic rd_ptr_en;

    logic [DEPTH_LOG2:0] rd_ptr_gray;
    logic [DEPTH_LOG2:0] rd_ptr_gray_nxt;
    logic rd_ptr_gray_en;

    logic [DEPTH_LOG2:0] wr_ptr_gray_sync;

    assign empty = (rd_ptr_gray == wr_ptr_gray_sync);

    assign full = (wr_ptr_gray == (rd_ptr_gray_sync ^ FULL_MASK));

    assign wr_ready = !full; 
    assign we = wr_valid & wr_ready;

    assign rd_valid = !empty;
    assign re = 1'b1;

    assign wr_ptr_nxt = wr_ptr + 1;
    assign wr_ptr_en = we;

    assign wr_ptr_gray_nxt = wr_ptr_nxt ^ (wr_ptr_nxt >> 1);
    assign wr_ptr_gray_en = we;

    assign rd_ptr_nxt = rd_ptr + 1;
    assign rd_ptr_en = rd_valid & rd_ready;

    assign rd_ptr_gray_nxt = rd_ptr_nxt ^ (rd_ptr_nxt >> 1);
    assign rd_ptr_gray_en = rd_valid & rd_ready;

    //==============================
    // u_sdp_ram
    //==============================
    sdp_ram #(.WIDTH(WIDTH), .DEPTH(2**DEPTH_LOG2)) u_sdp_ram
    (
        .clk(wr_clk),
        .we(we),
        .wr_addr(wr_ptr[DEPTH_LOG2-1:0]),
        .wr_data(wr_data),
        .re(re),
        .rd_addr(rd_ptr[DEPTH_LOG2-1:0]),
        .rd_data(rd_data)
    );

    //==============================
    // u_d_ff_rd_ptr
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) u_d_ff_rd_ptr
    (
        .clk(rd_clk),
        .rst(rd_rst),
        .en(rd_ptr_en),
        .d(rd_ptr_nxt),
        .q(rd_ptr)
    );

    //==============================
    // u_d_ff_wr_ptr
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) u_d_ff_wr_ptr
    (
        .clk(wr_clk),
        .rst(wr_rst),
        .en(wr_ptr_en),
        .d(wr_ptr_nxt),
        .q(wr_ptr)
    );

    //==============================
    // u_d_ff_rd_ptr_gray
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) u_d_ff_rd_ptr_gray
    (
        .clk(rd_clk),
        .rst(rd_rst),
        .en(rd_ptr_gray_en),
        .d(rd_ptr_gray_nxt),
        .q(rd_ptr_gray)
    );

    //==============================
    // u_d_ff_wr_ptr_gray
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) u_d_ff_wr_ptr_gray
    (
        .clk(wr_clk),
        .rst(wr_rst),
        .en(wr_ptr_gray_en),
        .d(wr_ptr_gray_nxt),
        .q(wr_ptr_gray)
    );

    //==============================
    // u_sync_rd_ptr_gray
    //==============================
    sync #(.WIDTH(DEPTH_LOG2+1)) u_sync_rd_ptr_gray
    (
        .clk(wr_clk),
        .d(rd_ptr_gray),
        .q(rd_ptr_gray_sync)
    );

    //==============================
    // u_sync_wr_ptr_gray
    //==============================
    sync #(.WIDTH(DEPTH_LOG2+1)) u_sync_wr_ptr_gray
    (
        .clk(rd_clk),
        .d(wr_ptr_gray),
        .q(wr_ptr_gray_sync)
    );

endmodule
