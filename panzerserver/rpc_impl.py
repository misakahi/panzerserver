from panzerserver import panzer_pb2, panzer_pb2_grpc


class PanzerServicer(panzer_pb2_grpc.PanzerServicer):

    def __init__(self, controller):
        if not controller.is_initialized():
            raise RuntimeError("Controller is not initialized")
        self.controller = controller

    def Drive(self, request, context):
        if request.left_level == 0 and request.right_level == 0:
            print("got empty drive request")
        else:
            self.controller.drive(request.left_level, request.right_level)

        return panzer_pb2.DriveResponse(success=True)

    def MoveTurret(self, request, context):
        if request.rotation == 0 and request.updown == 0:
            print("got empty turret request")
        else:
            self.controller.move_turret(request.rotation, request.updown)

        return panzer_pb2.MoveTurretResponse(success=True)

    def Control(self, request, context):
        print(request)
        self.Drive(request.driveRequest, context)
        self.MoveTurret(request.moveTurretRequest, context)

        return panzer_pb2.DriveResponse(success=True)

    def SendPing(self, request, context):
        print("pingpong")
        return panzer_pb2.Pong()

