load('data_test.mat');
M=data;
N=zeros(3,21,21,21);
for i =1:10
    
    N(:,i*2,i,i) = 1;
end
size(M)
size(N)

diff = abs(M(1,:,:,:)-N(1,:,:,:));
sum(sum(sum(sum(diff))))
