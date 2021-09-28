`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/04/26 17:05:49
// Design Name: 
// Module Name: FIFOBank
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


module FIFOBank(
        input clk,              //ʱ��
        input rst,              //��λ
                                
        output full,            //����־
        output empty,           //�ձ�־
                                
        input we0,              //д����0д�ź�
        output wready0,         //д����0��д�ź�
        input [7:0] wdata0,     //д����0��Ҫд�������
                                
        input we1,              //д����1д�ź�
        output wready1,         //д����1��д�ź�
        input [7:0] wdata1,     //д����1��Ҫд�������
                                
        input re0,              //������0���ź�
        output rready0,         //������0�ɶ��ź�
        output [7:0] rdata0,    //������0����������
                                
        input re1,              //������1���ź�
        output rready1,         //������1�ɶ��ź�
        output [7:0] rdata1     //������1����������
    );
    
    reg [2:0] waddr;
    reg [2:0] raddr;
    
    reg has;
    
    assign full = ((has==1'b1 && waddr == raddr) ? 1'h1 : 1'b0) | rst;
    assign empty = ((has==1'b0 && raddr == waddr) ? 1'b1 : 1'b0) | rst;
    
    
    wire [7:0] wdata;
    assign wdata = we0==1'b1 ? wdata0 : (we1==1'b1 ? wdata1 : 8'h0);
    assign wready0 = ((full==1'b0 || waddr+3'h1==raddr)) ? 1'b1 : 1'b0;
    assign wready1 = ((full==1'b0 || waddr+3'h1==raddr)&&we0==1'b0) ? 1'b1 : 1'b0;
    
    wire [7:0] rdata;
    assign rdata0 = re0 == 1'b1 ? rdata : 8'hzz;
    assign rdata1 = re0 == 1'b1 ? 8'h0  : (re1 == 1'b1 ? rdata : 8'hzz);
    assign rready0 = (empty==1'b0) ? 1'b1 : 1'b0;
    assign rready1 = (empty==1'b0&&re0==1'b0) ? 1'b1 : 1'b0; 
    
//    reg [5:0] cnt;
    always @(posedge clk) begin
        if(rst == 1'b1) begin
            waddr <= 3'h0;
            raddr <= 3'h0;
            has <= 1'b0;
//            cnt <= 6'h0;
        end else begin
            if(full==1'b0 && (we0 == 1'b1 || we1 == 1'b1)) begin
                waddr <= waddr + 3'h1;
                has <= 1'b1;
//                cnt <= cnt + 6'h1;
            end
            if(empty==1'b0 && (re0 == 1'b1 || re1 == 1'b1)) begin
                raddr <= raddr + 3'h1;
                has <= 1'b0;
//                cnt <= cnt - 6'h1;
            end
//            if((full==1'b0 && (we0 == 1'b1 || we1 == 1'b1))&&(empty==1'b0 && (re0 == 1'b1 || re1 == 1'b1)))
//                cnt <= cnt;
        end
    end
    
    FIFO_Line fifo (
      .a({1'b0, waddr}),        // input wire [3 : 0] a
      .d(wdata),        // input wire [7 : 0] d
      .dpra({1'b0, raddr}),  // input wire [3 : 0] dpra
      .clk(clk),    // input wire clk
      .we((~full) & (we0 | we1)),      // input wire we
      .dpo(rdata)    // output wire [7 : 0] dpo
    );
    
endmodule
