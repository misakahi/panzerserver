from concurrent import futures
import time
import grpc

from panzerserver import panzer_pb2_grpc, panzer
from panzerserver.rpc_impl import PanzerServicer


def main():
    # TODO use argparse

    # Setup thread pool
    executor = futures.ThreadPoolExecutor(max_workers=10)

    # Setup contoller
    print("setting up controller")
    controller = panzer.Controller(
        1, 2, None,     # left wheel
        4, 5, None,     # right wheel
    )
    controller.watch_configure(1000/3, 1000)    # remove me later
    executor.submit(controller.watch_loop)      # start watch loop

    # Setup gRPC server
    print("setting up server")
    server = grpc.server(executor)
    panzer_pb2_grpc.add_PanzerServicer_to_server(PanzerServicer(controller), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    print("server has started")

    try:
        while True:
            time.sleep(60*60*24)  # sleep for a day
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()