import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty, String
from geometry_msgs.msg import Twist

class DroneControlPublishers(Node):
    def __init__(self):
        super().__init__('drone_control_publishers')
        
        # Publishers
        self.takeoff_pub = self.create_publisher(Empty, '/takeoff', 10)
        self.land_pub = self.create_publisher(Empty, '/land', 10)
        self.emergency_pub = self.create_publisher(Empty, '/emergency', 10)
        self.control_pub = self.create_publisher(Twist, '/control', 10)
        self.move_pub = self.create_publisher(String, '/move', 10)  # New publisher for move commands
        self.flip_pub = self.create_publisher(String, '/flip', 10)  # Publisher for flip commands
        
        self.get_logger().info('Drone Control Publishers initialized')

    def publish_takeoff(self):
        self.takeoff_pub.publish(Empty())
        self.get_logger().info('Published: Takeoff')

    def publish_land(self):
        self.land_pub.publish(Empty())
        self.get_logger().info('Published: Land')

    def publish_emergency(self):
        self.emergency_pub.publish(Empty())
        self.get_logger().info('Published: Emergency')

    def publish_control(self, linear_x, linear_y, linear_z, angular_z):
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.linear.y = float(linear_y)
        msg.linear.z = float(linear_z)
        msg.angular.z = float(angular_z)
        self.control_pub.publish(msg)
        self.get_logger().info(f'Published: Control command ({linear_x}, {linear_y}, {linear_z}, {angular_z})')

    def publish_stop_move(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.z = 0.0
        self.control_pub.publish(msg)
        self.get_logger().info('Published: Control command (stop)')

    def publish_move(self, direction, distance):
        msg = String()
        msg.data = f"{direction} {distance}"
        self.move_pub.publish(msg)
        self.get_logger().info(f'Published: Move {direction} {distance} cm')

    def publish_flip(self, direction):
        msg = String()
        msg.data = direction
        self.flip_pub.publish(msg)
        self.get_logger().info(f'Published: Flip {direction}')

def main(args=None):
    rclpy.init(args=args)
    node = DroneControlPublishers()
    
    print("Drone Control Commands:")
    print("t - Takeoff")
    print("l - Land")
    print("e - Emergency")
    print("c x y z r - Control (x, y, z linear velocities, r angular velocity)")
    print("s - Control stop moving")
    print("m direction distance - Move (direction: up, down, left, right, forward, back; distance in cm)")
    print("f direction - Flip (direction: l, r, f, b)")
    print("q - Quit")

    try:
        while True:
            command = input("Enter command: ").split()
            if not command:
                continue
            
            if command[0] == 't':
                node.publish_takeoff()
            elif command[0] == 'l':
                node.publish_land()
            elif command[0] == 'e':
                node.publish_emergency()
            elif command[0] == 'c' and len(command) == 5:
                node.publish_control(*command[1:])
            elif command[0] == 's':
                node.publish_stop_move()
            elif command[0] == 'm' and len(command) == 3:
                node.publish_move(command[1], command[2])
            elif command[0] == 'f' and len(command) == 2:
                node.publish_flip(command[1])
            elif command[0] == 'q':
                break
            else:
                print("Invalid command. Please try again.")
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()