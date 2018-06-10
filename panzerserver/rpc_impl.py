from panzerserver import panzer_pb2, panzer_pb2_grpc


class PanzerServicer(panzer_pb2_grpc.PanzerServicer):

    def __init__(self, controller):
        if not controller.is_initialized():
            raise RuntimeError("Controller is not initialized")
        self.controller = controller

    def Drive(self, request, context):
        self.controller.drive(request.l_level, request.r_level)
        print(request)
        return panzer_pb2.DriveResponse(success=True)
