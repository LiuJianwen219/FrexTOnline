`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/11/04 10:38:14
// Design Name: 
// Module Name: dataReader
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module dataReader(
    input clk_100mhz,
    input clk,
    input [63:0] seg,
    input [15:0] led,
    output [4:0] data,
    output [3:0] s
    );
    
    reg [31:0] count;
    reg busy;
    reg [1:0] clk_reg;
    always @(posedge clk_100mhz) begin
        clk_reg = {clk_reg[0], clk};
    end
    
    always @(posedge clk_100mhz) begin
        if(clk_reg == 2'b01) begin
            count <= 32'b0;
            busy  <= 1'b1;
        end else begin
            if(count<32'd10_000_000)
                count <= count+32'b01;
            else // means free for 0.67s
                busy <= 1'b0;
        end
    end
    
    reg [63:0] segR;
    reg [15:0] ledR;
    reg [15:0] dataR;
    reg [3:0]  state;
    always @(posedge clk_100mhz) begin
        if(clk_reg == 2'b01) begin
            if(busy == 1'b0) begin
                state <= 4'h0;
                segR <= seg;
                ledR <= led;
            end else begin
                dataR <= {segR[63:60], ledR[15:15]};
    //            segR  <= {segR[59:0], segR[63:60]};
                segR  <= {segR[59:0], 4'b0};
    //            ledR  <= {ledR[14:0], ledR[15:15]};
                ledR  <= {ledR[14:0], 1'b0};
                state <= state + 4'h1;
    //            if(state==4'hf) begin // 如果没有中断显示那么就在最后一个状态读入新的数据
    //                state <= 4'h0;
    //                segR <= seg;
    //                ledR <= led;
    //            end
            end
        end
    end
    assign data = dataR;
    assign s = state;
    
endmodule
