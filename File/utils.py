import json
import requests
import logging
import config

logger = logging.getLogger(__name__)


def post_experiment(values, file):
    logger.info("Try to post EXPERIMENT with values: " + json.dumps(values))

    url = config.file_server_url + config.experiment_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_experimentType: values[config.c_experimentType],
        config.c_experimentId: values[config.c_experimentId],
        config.c_fileName: values[config.c_fileName],
    }
    print(values)

    files = {'file': file}
    r = requests.post(url, files=files, data=values)
    if r.status_code.__str__() != "200":
        logger.error("Post Experiment failed: request status not health: " + r.headers.__str__())
        return config.request_failed
    return config.request_success


def post_bit(values, file):
    logger.info("Try to post online BIT with values: " + json.dumps(values))

    url = config.file_server_url + config.online_BIT_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_experimentType: values[config.c_experimentType],
        config.c_experimentId: values[config.c_experimentId],
        config.c_compileId: values[config.c_compileId],
    }
    print(values)

    files = {'file': file}
    r = requests.post(url, files=files, data=values)
    if r.status_code.__str__() != "200":
        logger.error("Post Experiment failed: request status not health: " + r.headers.__str__())
        return config.request_failed
    return config.request_success


def delete_experiment(values):
    logger.info("Try to delete EXPERIMENT with values: " + json.dumps(values))

    url = config.file_server_url + config.experiment_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_experimentType: values[config.c_experimentType],
        config.c_experimentId: values[config.c_experimentId],
        config.c_fileName: values[config.c_fileName],
    }
    print(values)

    r = requests.delete(url, data=values)
    if r.status_code.__str__() != "200":
        logger.error("Post Experiment failed: request status not health: " + r.headers.__str__())
        return config.request_failed
    return config.request_success
