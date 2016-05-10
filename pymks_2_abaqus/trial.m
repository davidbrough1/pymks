clear
clc
close all

load('data.mat');
M=data;

% M=zeros(el^3,3);
% M(:,2)=ones(el^3,1);
% M(4631,1)=1;
% M(4631,2)=0;
% M(:,3:10)=round(rand(el^3,8));


% save M.mat M
size_ = size(M);
el=double(int8(size_(1) ^ (1 / 3)));
n_samples = size_(2);

nodesets(el);
fprintf('Data set loaded\n')

first50=fopen('50top.inp','r');
bottom50=fopen('50bottom.inp','r');

A=fread(first50,inf);
B=fread(bottom50,inf);

fclose(first50);
fclose(bottom50);

nodesetspbc=fopen('nodesets.inp','r');
nodesetspbcx=fread(nodesetspbc,inf);
fclose(nodesetspbc);

for ii=1:n_samples
    twopstatset(ii,M);
    matsets=fopen(['matset' int2str(ii) '.inp'],'r');
    materset=fread(matsets,inf);
    combined=fopen([int2str(el) '_' int2str(ii) '_fibers.inp'],'w+');
    fwrite(combined,A);
    fprintf(combined,'\n');
    fwrite(combined,nodesetspbcx);
    fprintf(combined,'\n');
    fwrite(combined,materset);
    fprintf(combined,'\n');
    fwrite(combined,B);
    fclose(matsets);
    fclose(combined);
    materialsets=['matset' int2str(ii) '.inp'];
    delete(materialsets);
    fprintf('Done inp %i\n',ii)
end

fclose('all');