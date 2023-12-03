import numpy as np
import re


def part1(data, data_array):

    number_regex = re.compile(r'\d{1,4}')
    total_sum = 0

    for i,row in enumerate(data):
        for n in re.finditer(number_regex,row):

            value = int(n.group())

            # Get context boundaries with edge cases
            if i==0:
                (up_limit,down_limit) = (0,i+2)
            elif i==len(data)-1:
                (up_limit,down_limit) = (i-1,i+1)
            else:
                (up_limit,down_limit) = (i-1,i+2)

            if n.start()==0:
                (left_limit,right_limit) = (0,n.end()+1)
            elif n.end()==len(row):
                (left_limit,right_limit) = (n.start()-1,n.end())
            else:
                (left_limit,right_limit) = (n.start()-1,n.end()+1)
                                        
            # Get context
            context = data_array[up_limit:down_limit,left_limit:right_limit]

            # Check for special symbols
            found_sym = np.where((~np.char.isdigit(context))&(context!='.'))[0]

            if len(found_sym)>0:
                total_sum += value
        
    print(f'The sum of all detected elements in part 1 is {total_sum}')


def part2(data, data_array):
    gear_regex = re.compile(r'\*{1}')
    number_regex = re.compile(r'\d{1,4}')
    total_sum = 0

    for i,row in enumerate(data):
            for gear in re.finditer(gear_regex,row):
                (n1,n2) = (0,0)
                # Get number coordinates
                global_pose = (i,gear.start())

                # Get context boundaries with edge cases
                if i==0:
                    (up_limit,down_limit) = (0,i+2)
                elif i==len(data)-1:
                    (up_limit,down_limit) = (i-1,i+1)
                else:
                    (up_limit,down_limit) = (i-1,i+2)

                if gear.start()==0:
                    (left_limit,right_limit) = (0,gear.end()+1)
                elif gear.end()==len(row):
                    (left_limit,right_limit) = (gear.start()-1,gear.end())
                else:
                    (left_limit,right_limit) = (gear.start()-1,gear.end()+1)
                                            
                # Get context
                context = data_array[up_limit:down_limit,left_limit:right_limit]
                
                # Check for numbers
                found_num_v = list(set(np.where(np.char.isdigit(context))[0]))
                found_num_h = list(set(np.where(np.char.isdigit(context))[1]))
              
                # If there are less or more than 2 numbers, skip
                if len(found_num_v)>2 and len(found_num_h)>2:
                    continue
                if len(found_num_v)<2 and len(found_num_h)<2:
                    continue
                # Check that if all numbers are in the same row, they are not adjacent
                if len(found_num_v) == 1 and len(found_num_h) == 3:
                    continue
                if len(found_num_v) == 1 and len(found_num_h) == 2:
                    if (np.abs(found_num_h[0] - found_num_h[1])) == 1:
                        continue

                # See if the numbers are in the same row
                if len(found_num_v)==1:
                    n1_row = data[global_pose[0]+found_num_v[0]-1]
                    n2_row = n1_row
                else:
                    n1_row = data[global_pose[0]+found_num_v[0]-1]
                    n2_row = data[global_pose[0]+found_num_v[1]-1]

                for n in re.finditer(number_regex,n1_row):
                    if (n.start()>=global_pose[1]-1 and n.start()<=global_pose[1]+1) or \
                        (n.end()>=global_pose[1] and n.end()<=global_pose[1]+2):
                        n1 = int(n.group())
                        n1_pos = (n.start(),n.end())
                        break
                    
                for n in re.finditer(number_regex,n2_row):
                    if (n.start()>=global_pose[1]-1 and n.start()<=global_pose[1]+1) or \
                        (n.end()>=global_pose[1] and n.end()<=global_pose[1]+2):
                        n2 = int(n.group())
                        n2_pos = (n.start(),n.end())
                        if n2 == n1 and n2_pos==n1_pos:
                            continue
                        if n2 != 0:
                            break
                total_sum += n1*n2

    print(f'The sum of all detected gears in part 2 is {total_sum}')

if __name__ == "__main__":

    with open('input.txt','r') as fd:
        data = list(map(lambda x: x.strip(), fd.readlines()))
        data_array = np.array(list(map(list,data)))

    part1(data, data_array)
    part2(data, data_array)
    