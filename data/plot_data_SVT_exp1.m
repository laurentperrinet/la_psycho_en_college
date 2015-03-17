% script plot_data_SVT_exp2
% import data matrix (WARNING format xls is ok, but xlsx NOT!!)


data(find(isnan(data(1,:))),:)=[];

n_resp = length(data(1,:))-3;
size_values = unique(data(:,2));
ecc_values = unique(abs(data(:,1)));

for i=1:length(ecc_values)
    ecc=ecc_values(i);
    for j=1:length(size_values)
        size=size_values(j);
        
        sel_mat=data(abs(data(:,1))==ecc & data(:,2)==size,:);
        sel_resp = sel_mat(:,3:end);
        sel_resp_corr=(repmat(sel_resp(:,1),1,n_resp)-sel_resp(:,2:end)==0);
        
        psycho_mat(i,j) = mean(sel_resp_corr(:));
    end
end

figure;
hold on;
plot(repmat(size_values,1,3),psycho_mat','-o');