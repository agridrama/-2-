bagselect = rosbag('_2024-05-16-15-09-44.bag');
bSel = select(bagselect,'Topic','/pressure/cal_and_ref_value');
msgStructs = readMessages(bSel,'DataFormat','struct');
msgs = readMessages(bSel);
%%
data = zeros(10000,6);
size(data)
for i = 1:10000
    m = msgs(i+5000);
    d = m{1};
    data(i,1:2) = d.Data(1:2);
    data(i,3:6) = d.Data(9:12).';
end
data(:,3:6) = data(:,3:6)/10.0;
%%
t = 1:10000;
t = t/500;
subplot(2,1,1)
plot(t,data(:,1:2))
ylabel("P / kPa")
title("入力用PAMの圧力")
legend("input1","input2")
subplot(2,1,2)
plot(t,data(:,3:6))
title("リザバーの出力値")
ylabel("P / kPa")
xlabel("t / s")
legend("output1","output2","output3","output4")