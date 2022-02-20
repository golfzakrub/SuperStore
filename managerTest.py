import  pandas as pd


class Manager():
    def readData(self,file):
        self.all_data = pd.read_csv(file,encoding = 'windows-1252').dropna()
        global namefile
        # namefile = file[file.index("/",-15,-1)+1:file.index(".")]
        # print(namefile)
        # self.showdata_head()
        # self.showdata_table()
        print(type(self.all_data))
        return self.all_data  

    def split_date(self,Dimension,all_data):
        Date_list = []
        split_list = []
        
        for i in Dimension:
            if "Date" in i:
                Date_list.append(i)
        for j in Date_list:
            split_list.append("split"+str(j))
        for x in range(len(Date_list)):
            if "-" in all_data[Date_list[x]][0]:
                split_list[x] = all_data[Date_list[x]].str.split("-",expand=True)
            if "/" in all_data[Date_list[x]][0]:
                split_list[x] = all_data[Date_list[x]].str.split("/",expand=True)
            ##### split %Y %M %D
            all_data[str(Date_list[x])+" Day"] = split_list[x][0]
            all_data[str(Date_list[x])+" Month"] = split_list[x][1]
            all_data[str(Date_list[x])+" Year"] = split_list[x][2]
            #### str to int
            all_data[str(Date_list[x])+" Day"].astype(int)
            all_data[str(Date_list[x])+" Month"].astype(int)
            all_data[str(Date_list[x])+" Year"].astype(int)  
        
        return all_data