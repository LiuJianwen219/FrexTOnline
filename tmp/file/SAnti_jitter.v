`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    21:03:38 04/29/2014 
// Design Name: 
// Module Name:    Anti_jitter 
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
module   SAnti_jitter(input wire clk, 
							 input wire RSTN,
							 input wire readn,
							 input wire [4:0]Key_y,
							 output reg [4:0] Key_x,
							 input wire [15:0]SW, 
							 output reg [4:0] Key_out,
							 output reg      Key_ready,
							 output reg [4:0] pulse_out,
							 output reg [4:0] BTN_OK,
							 output reg [15:0]SW_OK,
							 output reg 	  CR,
							 output reg 	  rst
							);

reg [31:0] counterState;		//#					

reg [31:0] counter, counter1, rst_counter;
reg [4:0]  btn_temp;
reg [15:0] sw_temp;
reg [2:0]  pulse,clk1;
wire [4:0] Keyy;
reg [1:0]  rdn;
reg scan, RSTN_temp;

	assign Keyy = ~Key_y;
	always@(posedge clk)
		clk1 <= clk1+1;
	wire CK = clk1[2];	
	
	always @(posedge CK) begin
		btn_temp <= Keyy;
		if(!readn )begin Key_ready <= 0;	Key_out <= 0;end

		if((btn_temp != Keyy ) && !scan) begin
			counter <= 32'h00000000;
			pulse <= 0;
			scan  <= 1;
			end
		else if(counter < 200_0000)begin 
				counter <= counter+1;
				counterState <= 32'b0;//#
				end//
				else begin
					if(~|Key_x)begin pulse_out <= Keyy; BTN_OK <= Keyy;  end
					if(~|Key_x && ~|Keyy )begin pulse_out <= 0; BTN_OK <= Keyy; end
					if(scan)	begin	
						case(Key_x)	
							  5'b00000: //Key_x <= 5'b11110;
											begin
												if(counterState < 125000)
													counterState <= counterState + 32'b1;
												else begin
													Key_x <= 5'b11101;
													counterState <= 32'b0;
												end
											end
							  5'b11101: begin
												if(counterState < 125000)
													counterState <= counterState + 32'b1;
												else begin
													if(~|Keyy) Key_x <= 5'b11011;
													else begin 
													Key_out <= {Keyy[4],3'h0,Keyy[4]}+Keyy_num(Keyy)+0;
													scan <= 0;  
													Key_x <= 5'b00000;
													Key_ready <=1;
													end
													counterState <= 32'b0;
												end
											end
											/*
											if(~|Keyy) Key_x <= 5'b11011;
										   else begin 
										   Key_out <= {Keyy[4],3'h0,Keyy[4]}+Keyy_num(Keyy)+0;
										   scan <= 0;  
										   Key_x <= 5'b00000;
										   Key_ready <=1;
										   end
											*/
							  5'b11011: begin
												if(counterState < 125000)
													counterState <= counterState + 32'b1;
												else begin
													if(~|Keyy)Key_x <= 5'b10111;
													else begin 
													Key_out <= {1'b0, {3{Keyy[4]}},1'b0}+Keyy_num(Keyy)+4; 
													scan <= 0; 
													Key_x <= 5'b00000;
													Key_ready <=1;
													end
													counterState <= 32'b0;
												end
											end
											/*
											if(~|Keyy)Key_x <= 5'b10111;
										   else begin 
										   Key_out <= {1'b0, {3{Keyy[4]}},1'b0}+Keyy_num(Keyy)+4; 
										   scan <= 0; 
										   Key_x <= 5'b00000;
										   Key_ready <=1;
										   end
											*/
							  5'b10111: begin
												if(counterState < 125000)
													counterState <= counterState + 32'b1;
												else begin
													if(~|Keyy) Key_x <= 5'b01111;
													else begin 
													Key_out <= {1'b0,Keyy[4],1'b0,{2{Keyy[4]}}}+Keyy_num(Keyy)+8; 
													scan <= 0;
													Key_x <= 5'b00000;
													Key_ready <=1;
													end
													counterState <= 32'b0;
												end
											end
											/*
											if(~|Keyy) Key_x <= 5'b01111;
										   else begin 
										   Key_out <= {1'b0,Keyy[4],1'b0,{2{Keyy[4]}}}+Keyy_num(Keyy)+8; 
										   scan <= 0;
										   Key_x <= 5'b00000;
										   Key_ready <=1;
										   end
											*/
							  5'b01111: begin
												if(counterState < 125000)
													counterState <= counterState + 32'b1;
												else begin
													if(~|Keyy) Key_x <= 5'b11110;
													else begin 
													Key_out <= {1'b0, Keyy[4],3'b000}+ Keyy_num(Keyy)+12; 
													scan <= 0;
													Key_x <= 5'b00000;
													Key_ready <=1;
													end
													counterState <= 32'b0;
												end
											end
											/*
											if(~|Keyy) Key_x <= 5'b11111;
										   else begin 
										   Key_out <= {1'b0, Keyy[4],3'b000}+ Keyy_num(Keyy)+12; 
										   scan <= 0;
										   Key_x <= 5'b00000;
										   Key_ready <=1;
										   end
											*/
							  5'b11110: begin
												if(counterState < 125000)
													counterState <= counterState + 32'b1;
												else begin
													if(~|Keyy) Key_x <= 5'b11111; 
													else begin 
													Key_out <= Keyy_num(Keyy)+16;
													scan <= 0; 
													Key_x <= 5'b00000;
													Key_ready <=1;
													end
													counterState <= 32'b0;
												end
											end
											/*
											if(~|Keyy) Key_x <= 5'b11101; 
										   else begin 
										   Key_out <= Keyy_num(Keyy)+16;
										   scan <= 0; 
										   Key_x <= 5'b00000;
										   Key_ready <=1;
										   end
											*/
								default: begin Key_out <= Key_out; 
											Key_x <= 5'b00000; 
											scan <= 0;
											end
						endcase
				end
			end
	 end



//========rst & SW
	always @(posedge clk) begin
		RSTN_temp <= RSTN;
		sw_temp <= SW; 
		if(RSTN_temp !=RSTN || sw_temp !=SW) begin
			counter1 <= 32'h00000000;
			rst_counter<=0;
			end
		else if(counter1<200_0000) 
				counter1<=counter1+1;
				else begin
					CR <= ~RSTN;
					SW_OK <= SW; 
				
					if(!RSTN && rst_counter<10000_0000)begin 
						rst_counter <= rst_counter + 1;
					end
					else begin 
						rst <= ~RSTN;
					end
				end
	 end



	function [4:0] Keyy_num;
		input [4:0] Keyy;		
		begin
		case (Keyy)
				
				5'b00000 : Keyy_num = 5'b00000;		// 
				5'b00001 : Keyy_num = 5'b00000;		// col0
				5'b00010 : Keyy_num = 5'b00001;		// col1
				5'b00100 : Keyy_num = 5'b00010;		// col2
				5'b01000 : Keyy_num = 5'b00011;		// col3
				5'b10000 : Keyy_num = 5'b00100;		// col4				
		endcase
		end
	endfunction
	 
endmodule
