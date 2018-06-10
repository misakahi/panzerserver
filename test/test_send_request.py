import grpc
import time

import panzerserver.panzer_pb2
import panzerserver.panzer_pb2_grpc


channel = grpc.insecure_channel('localhost:50051')
stub = panzerserver.panzer_pb2_grpc.PanzerStub(channel)

request = panzerserver.panzer_pb2.DriveRequest(l_level=1)
response = stub.Drive(request)
print(response)

for _ in range(10):
    response = stub.Drive(request)
    print(response)
    time.sleep(333/1e3)
