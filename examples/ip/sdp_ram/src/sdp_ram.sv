//==============================================
// sdp_ram
//==============================================
module sdp_ram
#(
    parameter WIDTH = 1,
    parameter DEPTH = 1
)
(
    input clk,
    input we,
    input [$clog2(DEPTH)-1:0] wr_addr,
    input [WIDTH-1:0] wr_data,
    input re,
    input [$clog2(DEPTH)-1:0] rd_addr,
    output logic [WIDTH-1:0] rd_data
);

    logic [WIDTH-1:0] memory [DEPTH-1:0];
    
    assign rd_data = re ? memory[rd_addr] : {WIDTH{1'bx}};
    
    always_ff @(posedge clk)
    begin
        memory[wr_addr] <= we ? wr_data : memory[wr_addr];
    end

endmodule
