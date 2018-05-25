import os

from flask import Flask, jsonify

from Yusi.YuConfig.config import GetConfig, GetDatabaseConnection,\
  GetCityVisitFinder, GetCorsOrigin, GetServerParams, GetTaskWorkerParams
from Yusi.YuServer.server import Server
from Yusi.YuServer.cors import crossdomain


config_filepath = os.environ['YUSI_CONFIG_FILE']
config = GetConfig(config_filepath)

database_connection = GetDatabaseConnection(config)
city_visit_finder = GetCityVisitFinder(config, database_connection)
cors_origin = GetCorsOrigin(config)
server_port, server_host = GetServerParams(config)
idle_seconds_terminate = GetTaskWorkerParams(config)

server = Server(database_connection, city_visit_finder, idle_seconds_terminate)

application = Flask(__name__)
application.secret_key = 'yusi_flask_secret_key'


@application.route('/ping', methods=['GET'])
@crossdomain(origin=cors_origin, methods=['GET'])
def ping():
  response_simple, code = server.Ping()
  return jsonify(**response_simple), code


def main(argv):
  application.run(port=server_port, host=server_host)


if __name__ == '__main__':
  main(os.sys.argv)
