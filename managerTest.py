import  pandas as pd
import os
import json
import hashlib
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
        
        if len(Date_list) > 0:            
            return True           
        else:
            return False

    def get_backup(self,file):
        if os.path.exists(file) == False:
            self.backup_head()        
        with open(file,'r') as head_file:
            self.data_head = json.load(head_file)
        return self.data_head
    
    def getDataFilter(self,data,item): ##recive DataFilter from filterComplete
        filter_key = {}        
        filter_key[item] = data
        if len(filter_key[item]) > 0:
            return True
        else:
            return False  

    def readUnionData(self,filename,filename_union):
        if filename == "":
            return print("ERROR IMPORT FILE")
        self.data_1 = pd.read_csv(filename,encoding = 'windows-1252').dropna()
        self.data_2 = pd.read_csv(filename_union,encoding = 'windows-1252').dropna()
        if len(self.data_1.columns) == len(self.data_2.columns):
            for i in range(len(self.data_1.columns)):
                if self.data_1.columns[i] == self.data_2.columns[i] :
                    self.all_data = pd.concat([self.data_1,self.data_2],axis=0).drop_duplicates().reset_index(drop=True)
                    # self.showdata_head()
                    # self.showdata_table()
                    return len(self.all_data.index)

    def check_md5(self,namefile,filename,data_head):
        self.data_head = data_head
        if self.data_head[namefile]["md5"] == hashlib.md5(open(filename,'rb').read()).hexdigest():
            return True
        else:
            return False