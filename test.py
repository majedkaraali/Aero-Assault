

max_velocity = 4
velocity_on_angle=max_velocity/90

def calculate_velocity(angle):
    if angle > 90:
        fixed_angle=angle-90
        vel_x=fixed_angle*velocity_on_angle
        vel_y=max_velocity-vel_x
        vel_x=-vel_x
        

    elif angle<=90:
        vel_y=angle*velocity_on_angle
        vel_x=max_velocity-vel_y
        

    print(f"Angle: {angle} degrees -> vel_x:", {vel_x}, ", vel_y:", {vel_y})
    




test1 = calculate_velocity(90)
test2 = calculate_velocity(45)
test3 = calculate_velocity(0)
test4 = calculate_velocity(135)
test5 = calculate_velocity(180)



