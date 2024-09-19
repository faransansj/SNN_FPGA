module top (
    input wire clk,
    input wire rst,
    input wire uart_rx,
    output wire programming_done
);

    wire [7:0] uart_data;
    wire data_valid;
    wire icap_busy;

    uart_receiver_fpga_program uart_inst (
        .clk(clk),
        .rx(uart_rx),
        .data_out(uart_data),
        .valid(data_valid),
        .programming_done(programming_done)
    );

    icap_controller icap_inst (
        .clk(clk),
        .rst(rst),
        .bitstream_data(uart_data),
        .data_valid(data_valid),
        .programming_done(programming_done),
        .icap_busy(icap_busy)
    );
endmodule
