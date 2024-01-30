name_to_id = {}

with open('contactPlan/contact_plan_7d_name_to_id_mapping.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split()
        name_to_id[key] = value


contacts_to_remove = [('LEO_ran000_tan016', 'GST_lat-31_lon-64'),
('LEO_ran000_tan016', 'GST_lat-46_lon168'),
('LEO_ran000_tan016', 'GST_lat025_lon055'),
('LEO_ran000_tan016', 'GST_lat034_lon-118'),
('LEO_ran000_tan016', 'GST_lat064_lon-51'),
]

GST_to_keep = ['GST_lat-31_lon-64', 'GST_lat-46_lon168', 'GST_lat025_lon055', 'GST_lat034_lon-118', 'GST_lat064_lon-51']
HAPS_to_keep = ['HAP_lat-31_lon-64', 'HAP_lat-46_lon168', 'HAP_lat025_lon055', 'HAP_lat034_lon-118', 'HAP_lat064_lon-51']
LEOS_to_keep = ['LEO_ran000_tan016']
NODE_LABELS_to_keep = ['MOC'] + GST_to_keep + HAPS_to_keep + LEOS_to_keep
NODE_IDS_to_keep = []
for e in NODE_LABELS_to_keep:
    NODE_IDS_to_keep.append(name_to_id[e])

input_file = 'contactPlan/contact_plan_7d_node-ids.txt'
output_file = 'contactPlan/contact_plan_7d_node-ids_1LEO_5HAP_5GST.txt'

with open(input_file, 'r') as file:
    lines = file.readlines()

filtered_lines = []

for line in lines:
    columns = line.strip().split()

    add_contact = True

    # remove contacts between LEO and GS
    for contact_to_rm in contacts_to_remove:
        if(columns[4] == name_to_id[contact_to_rm[0]] and columns[5] == name_to_id[contact_to_rm[1]]):
            add_contact = False
            break
        if(columns[4] == name_to_id[contact_to_rm[1]] and columns[5] == name_to_id[contact_to_rm[0]]):
            add_contact = False
            break

    if add_contact and len(columns) >= 6 and columns[4] in NODE_IDS_to_keep and columns[5] in NODE_IDS_to_keep:
        columns[6] = '1'  # data rate to 1
        line2 = ' '.join(columns)
        filtered_lines.append(line2 + '\n')

with open(output_file, 'w') as file:
    file.writelines(filtered_lines)



