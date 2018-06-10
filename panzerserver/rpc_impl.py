from panzerserver import panzer_pb2, panzer_pb2_grpc


class PanzerServicer(panzer_pb2_grpc.PanzerServicer):

    def __init__(self, controller):
        if not controller.is_initialized():
            raise RuntimeError("Controller is not initialized")
        self.controller = controller

    def Drive(self, request, context):
        self.controller.drive(request.left_level, request.right_level)
        print(request)
        return panzer_pb2.DriveResponse(success=True)

    def Control(self, request, context):
        self.Drive(request.driveRequest, context)
        print(request)
        return panzer_pb2.DriveResponse(success=True)
