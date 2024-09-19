module icap_controller (
    input wire clk,
    input wire rst,
    input wire [7:0] bitstream_data,
    input wire data_valid,
    input wire programming_done,
    output reg icap_busy
);

    reg [31:0] icap_data;
    reg icap_valid;

    ICAPE2 #(
        .DEVICE_ID(32'h0362_0933), // FPGA 장치 ID
        .ICAP_WIDTH("X32")
    ) icap_inst (
        .I(icap_data),
        .WRITE(icap_valid),
        .BUSY(icap_busy),
        .O(),
        .CLK(clk)
    );

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            icap_data <= 0;
            icap_valid <= 0;
        end else if (data_valid && !icap_busy) begin
            icap_data <= {24'b0, bitstream_data};
            icap_valid <= 1;
        end else begin
            icap_valid <= 0;
        end
    end
endmodule
