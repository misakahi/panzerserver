from panzerserver import panzer_pb2, panzer_pb2_grpc
import logging


class PanzerServicer(panzer_pb2_grpc.PanzerServicer):

    def __init__(self, controller):
        if not controller.is_initialized():
            raise RuntimeError("Controller is not initialized")
        self.controller = controller

    def Drive(self, request: panzer_pb2.DriveRequest, context):
        if request.left_level == 0 and request.right_level == 0:
            logging.info("got empty drive request")
        else:
            logging.info(request)
            self.controller.drive(request.left_level, request.right_level)

        return panzer_pb2.DriveResponse(success=True)

    def MoveTurret(self, request: panzer_pb2.MoveTurretRequest, context):
        if request.rotation == 0 and request.updown == 0:
            logging.info("got empty turret request")
        else:
            logging.info(request)
            self.controller.move_turret(request.rotation, request.updown)

        return panzer_pb2.MoveTurretResponse(success=True)

    def Control(self, request: panzer_pb2.ControlRequest, context):
        logging.info(request)
        self.Drive(request.driveRequest, context)
        self.MoveTurret(request.moveTurretRequest, context)

        return panzer_pb2.DriveResponse(success=True)

    def SendPing(self, request: panzer_pb2.Ping, context):
        logging.info("ping: " + request.ping)
        return panzer_pb2.Pong(pong=request.ping)

