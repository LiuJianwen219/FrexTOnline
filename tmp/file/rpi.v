`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    17:24:03 09/13/2020 
// Design Name: 
// Module Name:    rpi 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module rpi(
	input clk_100mhz,
	input RSTN,
	input [15:0] SW,
	input [3:0] BTN_IN,
	input ps2_clk,
	input ps2_data,
	output [3:0] BTN_OUT,
	output LEDCLK,
	output LEDDT,
	output LEDEN,
	output SEGCLK,
	output SEGDT,
	output SEGEN,
	input SegLedClk,
	output [4:0] SegLedData
 );

	reg[31:0] data;
	wire[4:0] KCode;
	wire[4:0] K_ROW;
	wire[31:0] clkdiv;
	wire[15:0] SW_OK;
	wire rst;
	
	wire [63:0] seg64;
	wire [15:0] led16;

	assign BTN_OUT = K_ROW[4:1];

	clkdiv M1 (.clk(clk_100mhz),
	           .rst(rst),
			   .clkdiv(clkdiv));

   SAnti_jitter  M2 (.clk(clk_100mhz), 
                    .Key_y({1'b1, BTN_IN}), 
                    .readn(1'b1), 
                    .RSTN(RSTN), 
                    .SW(SW), 
                    .BTN_OK(), 
                    .CR(), 
                    .Key_out(KCode[4:0]), 
                    .Key_ready(), 
                    .Key_x(K_ROW[4:0]), 
                    .pulse_out(), 
                    .rst(rst), 
                    .SW_OK(SW_OK[15:0]));

    wire [9:0] ps2_code;
    wire ps2_ready;
    ps2 M3(.clk(clk_100mhz),
            .rst(SW_OK[0]),
            .ps2_clk(ps2_clk),
            .ps2_data(ps2_data),
            .ps2_code(ps2_code),
            .ps2_ready(ps2_ready));

   Display  M4 (.clk(clk_100mhz), 
               .flash(clkdiv[25]), 
               .Hexs(data), 
               .LES(8'h04), 
               .point(data[15:8]), 
               .rst(rst),
               .Start(clkdiv[10]), 
               .Tex(SW_OK[15]),
               .seg_clk(SEGCLK), 
               .seg_clrn(), 
               .SEG_PEN(SEGEN), 
               .seg_sout(SEGDT),
               .seg64(seg64));
	
   GPIO  M6 (.clk(clk_100mhz), 
            .EN(1'b1), 
            .P_Data(data[15:0]), 
            .rst(rst), 
            .Start(clkdiv[10]), 
            .GPIOf0(led16), 
            .led_clk(LEDCLK), 
            .led_clrn(), 
            .LED_PEN(LEDEN), 
            .led_sout(LEDDT));

    
    dataReader M7(
            .clk_100mhz(clk_100mhz),
            .clk(SegLedClk),
            .seg(seg64),
            .led(led16),
            .data(SegLedData));

	always @* begin
	   if(KCode != 5'b0000)
			data = {KCode[3:0], 2'b0, ps2_code, SW_OK[15:0]};
	end

endmodule
