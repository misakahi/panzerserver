import grpc
import time

import panzerserver.panzer_pb2
import panzerserver.panzer_pb2_grpc


channel = grpc.insecure_channel('localhost:50051')
stub = panzerserver.panzer_pb2_grpc.PanzerStub(channel)

for i in range(10):
    if i % 2 == 0:
        request = panzerserver.panzer_pb2.ControlRequest(
            driveRequest=panzerserver.panzer_pb2.DriveRequest(left_level=1)
        )
    else:
        request = panzerserver.panzer_pb2.ControlRequest()
    print(request)
    response = stub.Control(request)
    print(response)
    time.sleep(333/1e3)
