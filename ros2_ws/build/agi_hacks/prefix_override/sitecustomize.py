import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/leo/hackathon/agi_house_robotics/ros2_ws/install/agi_hacks'
