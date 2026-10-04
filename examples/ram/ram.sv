//==============================================
// ram
//==============================================
module ram
#(
    parameter WIDTH = 1,
    parameter DEPTH = 1
)
(
    input clk,
    input valid,
    input we,
    input [$clog2(DEPTH)-1:0] addr,
    input [WIDTH-1:0] wr_data,
    output logic [WIDTH-1:0] rd_data
);

logic [WIDTH-1:0] memory [DEPTH-1:0];

assign rd_data = memory[addr];

always_ff @(posedge clk)
begin
    memory[addr] <= valid & we ? wr_data : memory[addr];
end

endmodule
