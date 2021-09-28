`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    13:43:21 09/16/2016 
// Design Name: 
// Module Name:    Display 
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
module Display(input clk,
					input rst,
					input Start,
					input Tex,
					input flash,
					input [31:0]Hexs,
					input [7:0]point,
					input [7:0]LES,
					
					output seg_clk,
					output seg_sout,
					output SEG_PEN,
					output seg_clrn,
					output [63:0] seg64
					);
					
wire [63:0]a,b,o;	
	assign o = Tex ? ~a : ~b;
	assign seg64 = o;

					
	HexTo8SEG		SM1(.Hexs(Hexs),		
							 .points(point),
							 .LES(LES),
							 .flash(flash),
							 .SEG_TXT(a)
							 );
						 
	SSeg_map			SM3(.Disp_num({Hexs,Hexs}), 
                      .Seg_map(b)
							 );


	P2S 				#(.DATA_BITS(64),.DATA_COUNT_BITS(6),.DIR(1)) 
						  P7SEG (.clk(clk),
									.rst(rst),
									.Start(Start),
									.PData(o),
									.s_clk(seg_clk),
									.s_clrn(seg_clrn),
									.sout(seg_sout),
									.EN(SEG_PEN)
									);							 

endmodule
