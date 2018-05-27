import os

from flask import Flask, jsonify

from YuConfig import config as config_
from YuServer import server as server_
from YuServer import cors


config_filepath = os.environ['YUSI_CONFIG_FILE']
config = config_.GetConfig(config_filepath)

database_connection = config_.GetDatabaseConnection(config)
city_visit_finder = config_.GetCityVisitFinder(config, database_connection)
cors_origin = config_.GetCorsOrigin(config)
server_port, server_host = config_.GetServerParams(config)
idle_seconds_terminate = config_.GetTaskWorkerParams(config)

server = server_.Server(database_connection, city_visit_finder, idle_seconds_terminate)

application = Flask(__name__)
application.secret_key = 'yusi_flask_secret_key'


@application.route('/ping', methods=['GET'])
@cors.crossdomain(origin=cors_origin, methods=['GET'])
def ping():
  response_simple, code = server.Ping()
  return jsonify(**response_simple), code


def main(argv):
  application.run(port=server_port, host=server_host)


if __name__ == '__main__':
  main(os.sys.argv)
