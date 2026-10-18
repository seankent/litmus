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
    input in__valid,
    output logic in__ready,
    input [WIDTH-1:0] in__data,
    output logic out__valid,
    input out__ready,
    output logic [WIDTH-1:0] out__data
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
    in__ready = 1'b0;
    out__valid = 1'b0;
    out__data = data;
    data__nxt = data;
    cnt__nxt = cnt;
    state__nxt = state;

    case (state)
        //==============================
        // STATE__READY
        //==============================
        STATE__READY:
        begin
            in__ready = out__ready;
            out__valid = in__valid;
            out__data = in__valid ? in__data : HOLD_DATA ? data : {WIDTH{1'bx}};
            data__nxt = in__valid & in__ready ? in__data : data;
            cnt__nxt = rand_cnt - 1;
            state__nxt =
                in__valid & in__ready & (rand_stall < stall_prob) & (rand_cnt != '0) ? STATE__STALL :
                STATE__READY;
        end

        //==============================
        // STATE__STALL
        //==============================
        STATE__STALL:
        begin
            out__data = HOLD_DATA ? data : {WIDTH{1'bx}};
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

