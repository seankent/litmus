//==============================================
// sync
//==============================================
module sync
#(
    parameter WIDTH = 1,
    parameter SYNC_DEPTH = 3
)
(
    input clk,
    input [WIDTH-1:0] d,
    output [WIDTH-1:0] q
);

logic [SYNC_DEPTH-1:0][WIDTH-1:0] x;

assign q = x[SYNC_DEPTH-1];

always_ff @(posedge clk)
begin
   x <= {x[SYNC_DEPTH-2:0], d};
end

endmodule

