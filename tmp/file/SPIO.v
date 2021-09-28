`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:58:11 07/01/2012 
// Design Name: 
// Module Name:    Device_led 
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
module 		 GPIO(input clk,
						input rst,
						input Start,
						input EN,
						input [15:0] P_Data,
						output wire led_clk,
						output wire led_sout,
						output wire led_clrn,
						output wire LED_PEN,
						output reg[15:0] GPIOf0	= 16'hFFFF					 
						);

reg [15:0]LED;
// GPIO out use on LEDs & Counter-Controler read and write
	assign LED_out = LED;
	always @(negedge clk or posedge rst) 
		if(rst) GPIOf0 <= 16'hFFFF; 
		else if(EN)  GPIOf0 <= P_Data;	
			  else    GPIOf0 <= GPIOf0; 
//	wire [15:0] ff = {GPIOf0[7:5],GPIOf0[0]};
		
	P2S 	#(.DATA_BITS(16),.DATA_COUNT_BITS(4),.DIR(1)) 
		  PLED (.clk(clk),
				.rst(rst),
				.Start(Start),
				.PData(GPIOf0),
				.s_clk(led_clk),
				.s_clrn(led_clrn),
				.sout(led_sout),
				.EN(LED_PEN)
				);							 

	
endmodule
