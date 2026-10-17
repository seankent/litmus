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

    logic [$clog2(DEPTH+1)-1:0] get;
    logic [$clog2(DEPTH+1)-1:0] get__nxt;
    logic get__en;

    logic [$clog2(DEPTH+1)-1:0] put;
    logic [$clog2(DEPTH+1)-1:0] put__nxt;
    logic put__en;

    assign wr_ready = (get == 0) ? (put != DEPTH) : (put != (get - 1));
    assign we = wr_valid & wr_ready;

    assign rd_valid = (get != put);
    assign re = 1'b1;

    assign get__nxt = (get == DEPTH) ? 0 : get + 1;
    assign get__en = rd_valid & rd_ready;

    assign put__nxt = (put == DEPTH) ? 0 : put + 1;
    assign put__en = we;

    //==============================
    // ram
    //==============================
    sdp_ram #(.WIDTH(WIDTH), .DEPTH(DEPTH+1)) ram
    (
        .clk(clk),
        .we(we),
        .wr_addr(put),
        .wr_data(wr_data),
        .re(re),
        .rd_addr(get),
        .rd_data(rd_data)
    );

    //==============================
    // d_ff__get
    //==============================
    d_ff #(.WIDTH($clog2(DEPTH+1)), .RESET_VALUE(0)) d_ff__get
    (
        .clk(clk),
        .rst(rst),
        .en(get__en),
        .d(get__nxt),
        .q(get)
    );

    //==============================
    // d_ff__put
    //==============================
    d_ff #(.WIDTH($clog2(DEPTH+1)), .RESET_VALUE(0)) d_ff__put
    (
        .clk(clk),
        .rst(rst),
        .en(put__en),
        .d(put__nxt),
        .q(put)
    );

endmodule
