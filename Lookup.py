import Global as LFI
#Library for the Inqusitive 


class Cable:
    
    def __init__(self, Higher_assembly, Lower_assembly, Unique_identifier, loc1,loc2='NULL'):
        #use dictionary to determine the cable connectors from Higher and lower Assemblies
        #Have it lookup locations of photos
        self.high = Higher_assembly
        self.low = Lower_assembly
        self.id = Unique_identifier
        self.loc1 = loc1 
        if loc2 != 'NULL':
            self.loc2 = loc2 
        else:
            self.loc2 = False


default_dir = LFI.setup()

dir_files=LFI.get_files_in_directory(default_dir)
print(default_dir)
print(dir_files)
selected_directories=LFI.select_directories(default_dir)
High_ass=selected_directories[0]
Low_ass=selected_directories[1]
Low_ass_location=selected_directories[2]
print(Low_ass_location)
Accept_location=selected_directories[3]
Reject_location=selected_directories[4]
for item in selected_directories:
    print(item)
low_dir_files=LFI.get_files_in_directory_from_refrence(Low_ass_location,"3-30-2022")
print(low_dir_files)
unique_cables = set()
for file in low_dir_files:
    parts = file.split(' ')[0]
    unique_cables.add(parts)

# Create instances of Cable class
cables = []
for unique_id in unique_cables:
    temp_list = []
    for file in low_dir_files:
        if unique_id == file.split(' ')[0]:
            temp_list.append(file)
    temp_list_2 = []
    temp_list_3 = []
    if len(temp_list)>2:
        for item in temp_list:
            for item2 in temp_list:
                if item != item2:
                    if item.split(' ')[1] == item2.split(' ')[1]:
                        temp_list_2.append(item2)
                        temp_list_2.append(item)
                        found_match = True
                        break
            if found_match:
                break
        for item in temp_list:
            if item not in temp_list_2:
                temp_list_3.append(item)
        cable = Cable(High_ass, Low_ass, unique_id, temp_list_2, temp_list_3)
        cables.append(cable)
    else:
        if len(temp_list)==2:
            cable = Cable(High_ass, Low_ass, unique_id, temp_list)
            cables.append(cable)
print('yes')
compare_list=[]
for cable in cables:
    compare_list.append(cable.loc1)
    if cable.loc2 != False:
        compare_list.append(cable.loc2)



print (compare_list)
accepted_images, rejected_images=LFI.create_image_display(compare_list,Low_ass_location)
#print(LFI.create_borderless_window(compare_list,Low_ass_location))
print(f"Accepted: {accepted_images}\n")
print(f"Rejected: {rejected_images}")
            
            
            
            

                
                
                    




#LFI.create_borderless_window()