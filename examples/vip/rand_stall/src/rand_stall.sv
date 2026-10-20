//==============================================
// rand_stall
//==============================================
module rand_stall
#(
    parameter WIDTH = 1,
    parameter HOLD_DATA = 0
)
(
    input clk,
    input in_valid,
    output logic in_ready,
    input [WIDTH-1:0] in_data,
    output logic out_valid,
    input out_ready,
    output logic [WIDTH-1:0] out_data
);

localparam STATE_READY = 2'h0;
localparam STATE_STALL = 2'h1;

logic [31:0] stall_prob = '0;
logic [31:0] stall_min  = '0;
logic [31:0] stall_max  = '0;

logic [1:0] state;
logic [1:0] state_nxt;

logic [31:0] cnt;
logic [31:0] cnt_nxt;

logic [WIDTH-1:0] data;
logic [WIDTH-1:0] data_nxt;

logic [31:0] rand_stall;
logic [31:0] rand_cnt;

initial
begin
    state = STATE_READY;
    cnt = '0;
    data = '0;
    rand_stall = '0;
    rand_cnt = '0;
end

always_comb
begin
    in_ready = 1'b0;
    out_valid = 1'b0;
    out_data = data;
    data_nxt = data;
    cnt_nxt = cnt;
    state_nxt = state;

    case (state)
        //==============================
        // STATE_READY
        //==============================
        STATE_READY:
        begin
            in_ready = out_ready;
            out_valid = in_valid;
            out_data = in_valid ? in_data : HOLD_DATA ? data : {WIDTH{1'bx}};
            data_nxt = (in_valid === 1'b1) & (in_ready === 1'b1) ? in_data : data;
            cnt_nxt = rand_cnt - 1;
            state_nxt =
                (in_valid === 1'b1) & (in_ready === 1'b1) & (rand_stall < stall_prob) & (rand_cnt != '0) ? STATE_STALL :
                STATE_READY;
        end

        //==============================
        // STATE_STALL
        //==============================
        STATE_STALL:
        begin
            out_data = HOLD_DATA ? data : {WIDTH{1'bx}};
            cnt_nxt = cnt - 1;
            state_nxt =
                (cnt == '0) ? STATE_READY :
                STATE_STALL;
        end
    endcase
end

always_ff @(posedge clk)
begin
    state <= state_nxt;
    cnt <= cnt_nxt;
    data <= data_nxt;
    rand_stall <= $urandom_range(0, 99);
    rand_cnt <= $urandom_range(stall_min, stall_max);
end

endmodule

