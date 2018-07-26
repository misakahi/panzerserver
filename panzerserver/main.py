import argparse
from concurrent import futures
import time
import grpc
import pprint

from panzerserver import panzer_pb2_grpc, panzer
from panzerserver.rpc_impl import PanzerServicer
import panzerserver.config


def main():
    parser = argparse.ArgumentParser(description='Panzer Vor!!')
    parser.add_argument('--port', type=int, default=50051, help='port number (default: 50051)')
    parser.add_argument('--config', type=str, default=None, help='config file (optional)')
    args = parser.parse_args()

    # Setup thread pool
    executor = futures.ThreadPoolExecutor(max_workers=10)

    # Load config
    if args.config is None:
        config = panzerserver.config.DEFAULT_CONFIG
    else:
        config = panzerserver.config.load_config(args.config)
    print("config loaded:")
    pprint.pprint(config)

    # init components
    l_wheel = panzer.Wheel(*config["components"]["left_wheel"])
    r_wheel = panzer.Wheel(*config["components"]["right_wheel"])
    turret = panzer.Turret(*config["components"]["turret"])

    # Setup controller
    print("setting up controller")
    controller = panzer.Controller(l_wheel, r_wheel, turret)
    controller.initialize()
    controller.set_watch_threshold(config["watch_threshold"])
    executor.submit(controller.watch_loop)  # start watch loop

    # Setup gRPC server
    print("setting up server")
    server = grpc.server(executor)
    panzer_pb2_grpc.add_PanzerServicer_to_server(PanzerServicer(controller), server)
    address = '[::]:%d' % args.port
    server.add_insecure_port(address)
    server.start()

    print("server has started %s" % address)

    try:
        while True:
            time.sleep(60 * 60 * 24)  # sleep for a day
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()
