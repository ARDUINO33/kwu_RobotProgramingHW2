import time
import rclpy
from rclpy.node import Node as node
from rclpy.action import ActionServer

from interfaces.srv import Multiply
from interfaces.msg import Univid
from interfaces.action import Calc

class node1(node):
    def __init__(self):
        super().__init__('node1')
        self.publisher = self.create_publisher(Univid,'University_ID', 10) #퍼블리셔 생성, 큐크기 10
        self.srv = self.create_service(Multiply, 'multiply', self.calcMCallback) #서비스 서버 생성
        self.action_server = ActionServer(self, Calc, 'Calc_Action', self.actionCallback) #액션 서버 설정
        self.declare_parameter('uID', '2022741036') #파라미터 설정
        
        #타이머 주기, 카운터, 타이머 생성
        t_period = 0.5
        self.count = 0
        self.timer = self.create_timer(t_period, self.timerCallback)
        
    def calcMCallback(self, input, output):
        output.res = input.x * input.y
        self.get_logger().info('Incoming request\na: %d b: %d' % (input.x, input.y))
        
        return output
    
    def actionCallback(self, goal_handle):    #액션 동작(add digit)
        self.get_logger().info('Executing goal...')

        feedback_msg = Calc.Feedback()
        UID_ = goal_handle.request.univid
        feedback_msg.progress = [int(digit) for digit in UID_]

        tmp_sum = 0

        for digit in feedback_msg.progress:
            tmp_sum += digit
            feedback_msg.progress[0] = tmp_sum  #추가된 결과를 첫번째 진행 요소에 저장(수신된 UID와 추가된 결과를 모두 표시)
            self.get_logger().info('Feedback: [First element is partial sum] {0}'.format(feedback_msg.progress))
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Calc.Result()
        result.process = feedback_msg.progress
        return result
    
    def timerCallback(self):   #매개변수

        gotParam = self.get_parameter('uID').get_parameter_value().string_value      #parameter 설정
        
        newParam = rclpy.parameter.Parameter(
            'uID',
            rclpy.Parameter.Type.STRING,
            '2022741036'
        )
        allParam = [newParam]
        self.set_parameters(allParam)

        msg = Univid()     #publish uid
        msg.univid = gotParam + ': %d' % self.count
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.univid)
        self.count += 1
        


def main(args=None):
    rclpy.init(args=args)

    nd1 = node1()

    rclpy.spin(nd1)

    nd1.destroy_node()
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
