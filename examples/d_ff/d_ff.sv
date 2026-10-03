//==============================================
// d_ff 
//==============================================
module d_ff 
#(
    parameter WIDTH = 1,
    parameter RESET_VALUE = 0
)
(
    input clk,
    input rst,
    input en,
    input [WIDTH-1:0] d,
    output logic [WIDTH-1:0] q
);

always_ff @(posedge clk)
begin
    q <= rst ? RESET_VALUE : en ? d : q; 
end

endmodule
