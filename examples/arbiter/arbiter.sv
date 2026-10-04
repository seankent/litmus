//==============================================
// arbiter
//==============================================
module arbiter
#(
    parameter N = 2
)
(
    input [N-1:0] req,
    output logic [N-1:0] gnt
);

assign gnt[N-1] = req[N-1];

generate
    for (genvar i = 0; i < N-1; i++)
    begin : g_gnt
        assign gnt[i] = req[i] & (req[N-1:i+1] == 0);
    end
endgenerate

endmodule
