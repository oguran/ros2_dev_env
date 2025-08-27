#!/usr/bin/env python3
# file: static_tf_resender.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from std_srvs.srv import Trigger

class StaticTFResender(Node):
    def __init__(self):
        super().__init__('static_tf_resender')
        self.broadcaster = StaticTransformBroadcaster(self)
        self.transforms = []

        # === ここに必要な static 変換を列挙（例） ===
        def mk(parent, child, xyz, quat):
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = parent
            t.child_frame_id = child
            t.transform.translation.x, t.transform.translation.y, t.transform.translation.z = xyz
            t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w = quat
            return t

        self.transforms.append(mk('base_link','camera_link',(0.0,0.0,0.1),(0,0,0,1)))
        self.transforms.append(mk('base_link','laser',(0.15,0.0,0.2),(0,0,0,1)))
        # ==========================================

        # 起動直後の複数回再送（500ms × 5 回）
        self._count = 0
        self._timer = self.create_timer(0.5, self._resend_once)
        self._resend_once()

        # 手動トリガ用サービス
        self._srv = self.create_service(Trigger, 'resend_static_tf', self._srv_cb)

    def _publish_all(self):
        # 1 メッセージにまとめて送る
        self.broadcaster.sendTransform(self.transforms)

    def _resend_once(self):
        self._publish_all()
        self._count += 1
        if self._count >= 5:
            self._timer.cancel()
            self.get_logger().info('Initial static TF re-send done')

    def _srv_cb(self, req, resp):
        self._publish_all()
        resp.success = True
        resp.message = 'static TF resent'
        return resp

def main():
    rclpy.init()
    node = StaticTFResender()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
