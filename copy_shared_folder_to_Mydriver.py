import time
from auth import second_auth
from fileinput import filename
from auth import ferst_auth


#Establish connection to your google drive Api
drive = ferst_auth()
service = second_auth()
# 


Files_paths_List = []
Files_Id_List = []

Subfolders_Path_List = []


def get_path_subfolders_and_files (Shared_Folder_Id,name):
    
    
    fileList = drive.ListFile({'q': "'%s' in parents and trashed=false"% (Shared_Folder_Id)}).GetList()
    
    for file in fileList:
        file_path = name+ file['title']
        if (file['mimeType']!='application/vnd.google-apps.folder'):
            Files_paths_List.append(file_path)
            Files_Id_List.append(file['id'])
        else:

            Subfolders_Path_List.append(file_path)
            
            get_path_subfolders_and_files(file['id'], file_path+"/")
    subfolders_paths = Subfolders_Path_List
    return subfolders_paths




        
   

      

def copy_files_to_MyDrive(file_id,parent_folder_id,file_Name) :
   
    
    parent_folder_id=parent_folder_id.replace('\n','')
    
    try:
        Source_file_id = file_id

        
        
        file_metadata = {
            'name':file_Name,
            'parents':[parent_folder_id],
            'starred':True,
            'description':'my file name'
        
            
        }
        service.files().copy(
            Files_Id_List=Source_file_id,
            body = file_metadata
        ).execute()  

    except Exception as errour:
        print("Erour"+str(errour))

def Get_Id_From_Link (Folder_link):
    
        link= Folder_link.split('/')
        link= link[-1]
        if '?' in link :
            link = link.split('?')
            folder_id = link[0]
        else :
            folder_id=link
        
        return  folder_id
 






def Creat_Subfolder_path_inside_MyDrive (name,parents):


    if(parents==''):
        
        file_metadata = {

        'name':name,
        'mimeType':'application/vnd.google-apps.folder',
        'parents':[]
        
    }

    else :
        try:
            
            
            file_metadata = {

            'name':name,
            'mimeType':'application/vnd.google-apps.folder',
            'parents':[parents]
            }
        except Exception as e:
            print('ereur : ' +str(e))   

     
    folder_id = service.files().create(body=file_metadata).execute()
 
    previeus_folder_id = folder_id.get('id')    
    
    
    with open("path.txt", "a") as file:
        file.write(name+':'+str(folder_id.get('id')) +"\n" )
    return previeus_folder_id    
   
               
        

def Check_subfolder_exect_inside_Mydrive(folder_path,MyFolder_Id) :
    
    folder_already_exect = False;
    
   
    parent_id = MyFolder_Id

    split_path = folder_path.split('/')
    
    i = 0
    for folder_name in split_path:
        
        file1 = open('path.txt', 'r')
        Lines = file1.readlines()
        file1.close()

        for line in Lines:
           
            exected_folder = line.split(':')

            

            
            if(split_path[i] == exected_folder[0] ):

               
                folder_already_exect = True
                exected_folder[1]=exected_folder[1].replace('\n','')
                parent_id = exected_folder[1]
                break;  
                
            else:
                
                folder_already_exect=False   
            
                
                

        if (folder_already_exect == False):
           
            parent_id=Creat_Subfolder_path_inside_MyDrive(folder_name,parent_id)
        i=i+1          
            

def start_copying_file_to_MyDrive(file_path):

    file2 = open('path.txt', 'r')
    Lines = file2.readlines()
    file2.close()

    parent_folders = file_path.split('/')

    i=len(parent_folders)
    
    parent_folder= parent_folders[i-2]
   
    files_count=0

    if(Lines==[]):
       
       print(Lines)

    else:
        for line in Lines :
            line_name_id=line.split(':')

            if(line_name_id[0]==parent_folder):
                
                copy_files_to_MyDrive(Files_Id_List[files_count],line_name_id[1],parent_folders[i-1])

                files_count+=1






    
if __name__ == '__main__':
   
    Shared_folder_Link = input('Enter Link to public folder you want to copy : ')
    MyDrive_folder_Link = input('Enter Link to folder you want to copy into : ')
    New_Shared_Folder_Name = input('give the copy folder a name :')

    Shared_Folder_Id = Get_Id_From_Link(Shared_folder_Link)
    MyFolder_Id = Get_Id_From_Link(MyDrive_folder_Link) 
    
    file = open("path.txt","w")
    file.close()

    subfolders_paths_List = get_path_subfolders_and_files(Shared_Folder_Id,New_Shared_Folder_Name+'/')
    
    print("\nStart Copying Folder tree structure into your Drive ..." )

    if( subfolders_paths_List==[]):
        Check_subfolder_exect_inside_Mydrive(New_Shared_Folder_Name,MyFolder_Id)
        
    else :
        for subfolder_path in  subfolders_paths_List:
            Check_subfolder_exect_inside_Mydrive(subfolder_path,MyFolder_Id)
    
            
    print("Folder tree structure Copied successfuly")
    print("Start Copying ...")

    for file_path in Files_paths_List :    
        start_copying_file_to_MyDrive(file_path)

    print("Files Copied successfuly")

    print ('shared Folder "'+ New_Shared_Folder_Name +'" Copied successfuly ' )
    




