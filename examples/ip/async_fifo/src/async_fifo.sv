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
    logic [DEPTH_LOG2:0] wr_ptr__nxt;
    logic wr_ptr__en;

    logic [DEPTH_LOG2:0] wr_ptr_gray;
    logic [DEPTH_LOG2:0] wr_ptr_gray__nxt;
    logic wr_ptr_gray__en;

    logic [DEPTH_LOG2:0] rd_ptr_gray_sync;

    logic [DEPTH_LOG2:0] rd_ptr;
    logic [DEPTH_LOG2:0] rd_ptr__nxt;
    logic rd_ptr__en;

    logic [DEPTH_LOG2:0] rd_ptr_gray;
    logic [DEPTH_LOG2:0] rd_ptr_gray__nxt;
    logic rd_ptr_gray__en;

    logic [DEPTH_LOG2:0] wr_ptr_gray_sync;

    assign empty = (rd_ptr_gray == wr_ptr_gray_sync);

    assign full = (wr_ptr_gray == (rd_ptr_gray_sync ^ FULL_MASK));

    assign wr_ready = !full; 
    assign we = wr_valid & wr_ready;

    assign rd_valid = !empty;
    assign re = 1'b1;

    assign wr_ptr__nxt = wr_ptr + 1;
    assign wr_ptr__en = we;

    assign wr_ptr_gray__nxt = wr_ptr__nxt ^ (wr_ptr__nxt >> 1);
    assign wr_ptr_gray__en = we;

    assign rd_ptr__nxt = rd_ptr + 1;
    assign rd_ptr__en = rd_valid & rd_ready;

    assign rd_ptr_gray__nxt = rd_ptr__nxt ^ (rd_ptr__nxt >> 1);
    assign rd_ptr_gray__en = rd_valid & rd_ready;

    //==============================
    // ram
    //==============================
    sdp_ram #(.WIDTH(WIDTH), .DEPTH(2**DEPTH_LOG2)) ram
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
    // d_ff__rd_ptr
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) d_ff__rd_ptr
    (
        .clk(rd_clk),
        .rst(rd_rst),
        .en(rd_ptr__en),
        .d(rd_ptr__nxt),
        .q(rd_ptr)
    );

    //==============================
    // d_ff__wr_ptr
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) d_ff__wr_ptr
    (
        .clk(wr_clk),
        .rst(wr_rst),
        .en(wr_ptr__en),
        .d(wr_ptr__nxt),
        .q(wr_ptr)
    );

    //==============================
    // d_ff__rd_ptr_gray
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) d_ff__rd_ptr_gray
    (
        .clk(rd_clk),
        .rst(rd_rst),
        .en(rd_ptr_gray__en),
        .d(rd_ptr_gray__nxt),
        .q(rd_ptr_gray)
    );

    //==============================
    // d_ff__wr_ptr_gray
    //==============================
    d_ff #(.WIDTH(DEPTH_LOG2+1), .RESET_VALUE(0)) d_ff__wr_ptr_gray
    (
        .clk(wr_clk),
        .rst(wr_rst),
        .en(wr_ptr_gray__en),
        .d(wr_ptr_gray__nxt),
        .q(wr_ptr_gray)
    );

    //==============================
    // sync__rd_ptr_gray
    //==============================
    sync #(.WIDTH(DEPTH_LOG2+1)) sync__rd_ptr_gray
    (
        .clk(wr_clk),
        .d(rd_ptr_gray),
        .q(rd_ptr_gray_sync)
    );

    //==============================
    // sync__wr_ptr_gray
    //==============================
    sync #(.WIDTH(DEPTH_LOG2+1)) sync__wr_ptr_gray
    (
        .clk(rd_clk),
        .d(wr_ptr_gray),
        .q(wr_ptr_gray_sync)
    );

endmodule
