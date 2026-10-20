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

localparam STATE__READY = 2'h0;
localparam STATE__STALL = 2'h1;

logic [31:0] stall_prob = '0;
logic [31:0] stall_min  = '0;
logic [31:0] stall_max  = '0;

logic [1:0] state;
logic [1:0] state__nxt;

logic [31:0] cnt;
logic [31:0] cnt__nxt;

logic [WIDTH-1:0] data;
logic [WIDTH-1:0] data__nxt;

logic [31:0] rand_stall;
logic [31:0] rand_cnt;

initial
begin
    state = STATE__READY;
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
    data__nxt = data;
    cnt__nxt = cnt;
    state__nxt = state;

    case (state)
        //==============================
        // STATE__READY
        //==============================
        STATE__READY:
        begin
            in_ready = out_ready;
            out_valid = in_valid;
            out_data = in_valid ? in_data : HOLD_DATA ? data : {WIDTH{1'bx}};
            data__nxt = (in_valid === 1'b1) & (in_ready === 1'b1) ? in_data : data;
            cnt__nxt = rand_cnt - 1;
            state__nxt =
                (in_valid === 1'b1) & (in_ready === 1'b1) & (rand_stall < stall_prob) & (rand_cnt != '0) ? STATE__STALL :
                STATE__READY;
        end

        //==============================
        // STATE__STALL
        //==============================
        STATE__STALL:
        begin
            out_data = HOLD_DATA ? data : {WIDTH{1'bx}};
            cnt__nxt = cnt - 1;
            state__nxt =
                (cnt == '0) ? STATE__READY :
                STATE__STALL;
        end
    endcase
end

always_ff @(posedge clk)
begin
    state <= state__nxt;
    cnt <= cnt__nxt;
    data <= data__nxt;
    rand_stall <= $urandom_range(0, 99);
    rand_cnt <= $urandom_range(stall_min, stall_max);
end

endmodule

