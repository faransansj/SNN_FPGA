module uart_receiver_fpga_program(
    input wire clk,
    input wire rx,
    output reg [7:0] data_out,
    output reg valid,
    output reg programming_done
);

    parameter BAUD_RATE = 115200;
    parameter CLOCK_FREQ = 100000000; // 100MHz 클럭
    parameter EXPECTED_BITSTREAM_SIZE = 100000; // 비트스트림 크기

    reg [15:0] baud_counter;
    reg [7:0] bit_index;
    reg receiving;
    reg [7:0] rx_shift_reg;

    reg [15:0] byte_counter;

    initial begin
        baud_counter = 0;
        bit_index = 0;
        receiving = 0;
        rx_shift_reg = 0;
        data_out = 0;
        valid = 0;
        programming_done = 0;
        byte_counter = 0;
    end

    always @(posedge clk) begin
        if (!receiving) begin
            if (!rx) begin
                receiving <= 1;
                baud_counter <= (CLOCK_FREQ / BAUD_RATE) / 2; 
            end
        end else begin
            baud_counter <= baud_counter - 1;
            if (baud_counter == 0) begin
                baud_counter <= CLOCK_FREQ / BAUD_RATE;
                if (bit_index < 8) begin
                    rx_shift_reg[bit_index] <= rx;
                    bit_index <= bit_index + 1;
                end else if (bit_index == 8) begin
                    data_out <= rx_shift_reg;
                    valid <= 1;
                    receiving <= 0;
                    bit_index <= 0;
                    byte_counter <= byte_counter + 1;
                end
            end
        end

        if (byte_counter == EXPECTED_BITSTREAM_SIZE) begin
            programming_done <= 1;
        end
    end
endmodule
