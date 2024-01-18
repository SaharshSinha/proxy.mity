import time
import motioner

wheel_radius_mm = 100
wheel_circumference = 22/7*wheel_radius_mm
total_distance_to_travel = 300

speed_outer = round(1 * 30)
speed_inner = round(1 * 17)

hasnt_moved_yet = True
direction = 1
travel_instrutions = [
    ( 45, 0, 0), 
    (100, -1 * speed_outer, speed_inner), 
    (100, speed_outer, -1 * speed_inner), 
    ( 10, 0, 0), 
    (100, -1 * speed_outer, speed_inner), 
    (100, speed_outer, -1 * speed_inner), 
    ( 10, 0, 0), 
    (100, -1 * speed_outer, speed_inner), 
    (100, speed_outer, -1 * speed_inner), 
    ( 10, 0, 0), 
    (100, -1 * speed_outer, speed_inner), 
    (100, speed_outer, -1 * speed_inner), 
    # (3, 20, -20), 
    # (30, 120, -120),
    # (15, 0, 0), 
    # (10, -20, 20), 
    # (30, -120, 120), 
    # (6, -120, 100), 
    # (6, -120, 30), 
    # (6, -120, 65), 
    # (6, -120, 100), 
    # (30, -120, 120), 
    # (10, 0, 0), 
    # (30, 120, -120), 
    # (6, 120, -100), 
    # (6, 120, -65), 
    # (6, 120, -30), 
    # (6, 120, -65), 
    # (6, 120, -100),
    # (30, 120, -120),
    # (10, 20, -20), 

]

travel_instrutions_count = len(travel_instrutions)

max_travel_index = 20

travel_instruction_index = 0
start_time = time.time()
total_time_elapsed = 0
next_time_threshold = 0
time_threshold_index = 0


def get_instructions():
    motioner.total_time_elapsed = round(float(time.time() - motioner.start_time), 1)
    
    if motioner.total_time_elapsed > motioner.next_time_threshold:
        motioner.next_instructions = travel_instrutions[time_threshold_index % travel_instrutions_count]
        motioner.next_time_threshold += motioner.next_instructions[0]
        print(f'Index {motioner.time_threshold_index} {time.time()} total_time_elapsed: {motioner.total_time_elapsed}')   
        motioner.time_threshold_index += 1
        if motioner.next_instructions[1] < 0:
            motioner.direction = 1
        else:
            motioner.direction = -1


# while (travel_instruction_index < max_travel_index):
# while (True):

#     total_time_elapsed = round(float(time.time() - start_time), 1)
    
#     if total_time_elapsed > next_time_threshold:
#          next_instructions = travel_instrutions[time_threshold_index]
#          next_time_threshold += next_instructions[0]
#          time_threshold_index += 1
#          print(f'{time.time()} total_time_elapsed: {total_time_elapsed}')
#     # print(f'{time.time()}')
#     # travel_index = travel_instruction_index % travel_instrutions_count
#     # current_instrution = travel_instrutions[travel_index]
#     # print(current_instrution)
#     # time.sleep(current_instrution[0])
#     # travel_instruction_index += 1
# while (True):
#     get_instructions()