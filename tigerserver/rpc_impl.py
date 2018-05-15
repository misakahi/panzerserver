from tigerserver import panzer_pb2, panzer_pb2_grpc


class PanzerServicer(panzer_pb2_grpc.PanzerServicer):

    def __init__(self, controller):
        self.controller = controller

    def Drive(self, request, context):
        self.controller.drive(request.l_level, request.r_level)
        print(request)
        return panzer_pb2.DriveResponse(success=True)
