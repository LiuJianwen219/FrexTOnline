import json
import os
import uuid

import requests
import logging
import config

logger = logging.getLogger(__name__)

# write file interface, maybe DFS future
def file_writer(fire_dir, file_name, file_content):
    if not os.path.exists(fire_dir):
        os.makedirs(fire_dir)
    with open(os.path.join(fire_dir, file_name), 'wb+') as destination:
        destination.write(file_content)
    if len(file_content)<1:
        return None
    return 1


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


def get_experiment(values, newFileName):
    logger.info("Try to get EXPERIMENT with values: " + json.dumps(values))

    url = config.file_server_url + config.experiment_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_experimentType: values[config.c_experimentType],
        config.c_experimentId: values[config.c_experimentId],
        config.c_fileName: values[config.c_fileName],
    }
    print(values)

    r = requests.get(url, params=values)
    if r.status_code.__str__() != "200":
        logger.error("Request SRC failed: " + r.headers.__str__())
        return None

    if r.headers['content-type'] == "application/octet-stream" and r.content:
        dest_direction = config.work_dir
        # dest_filename = values[config.c_fileName]
        if not file_writer(dest_direction, newFileName, r.content):
            return None
        return r.content
    return None


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


def get_bit(values):
    logger.info("Try to get online BIT with values: " + json.dumps(values))
    url = config.file_server_url + config.online_BIT_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_experimentType: values[config.c_experimentType],
        config.c_experimentId: values[config.c_experimentId],
        config.c_compileId: values[config.c_compileId],
    }
    r = requests.get(url, params=values)
    if r.status_code.__str__() != "200":
        logger.error("Request BIT failed: " + r.headers.__str__())
        return None

    if r.headers['content-type'] == "application/octet-stream" and r.content:
        return r.content
    return None


def get_log(values):
    logger.info("Try to get online Log with values: " + json.dumps(values))
    url = config.file_server_url + config.online_LOG_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_experimentType: values[config.c_experimentType],
        config.c_experimentId: values[config.c_experimentId],
        config.c_compileId: values[config.c_compileId],
    }
    r = requests.get(url, params=values)
    if r.status_code.__str__() != "200":
        logger.error("Request LOG failed: " + r.headers.__str__())
        return None

    if r.headers['content-type'] == "application/octet-stream" and r.content:
        return r.content
    return None


def post_course(values, file):
    logger.info("Try to post online COURSE with values: " + json.dumps(values))

    url = config.file_server_url + config.COURSE_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_courseId: values[config.c_courseId],
        config.c_courseTemplateId: values[config.c_courseTemplateId],
        config.c_courseTemplateExperimentId: values[config.c_courseTemplateExperimentId],
        config.c_fileName: values[config.c_fileName],
    }
    print(values)

    files = {'file': file}
    r = requests.post(url, files=files, data=values)
    if r.status_code.__str__() != "200":
        logger.error("Post Experiment failed: request status not health: " + r.headers.__str__())
        return config.request_failed
    return config.request_success


def get_course(values):
    url = config.file_server_url + config.COURSE_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_courseId: values[config.c_courseId],
        config.c_courseTemplateId: values[config.c_courseTemplateId],
        config.c_courseTemplateExperimentId: values[config.c_courseTemplateExperimentId],
        config.c_fileName: values[config.c_fileName],
    }
    r = requests.get(url, params=values)
    if r.status_code.__str__() != "200":
        logger.error("Request SRC failed: " + r.headers.__str__())
        return config.request_failed

    if r.headers['content-type'] == "application/octet-stream" and r.content:
        dest_direction = config.work_dir
        dest_filename = values[config.c_fileName]
        if not file_writer(dest_direction, dest_filename, r.content):
            return config.request_failed
        return config.request_success
    return config.request_failed


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


def delete_course(values):
    logger.info("Try to delete online COURSE with values: " + json.dumps(values))

    url = config.file_server_url + config.COURSE_API + "/"
    values = {
        config.c_userId: values[config.c_userId],
        config.c_courseId: values[config.c_courseId],
        config.c_courseTemplateId: values[config.c_courseTemplateId],
        config.c_courseTemplateExperimentId: values[config.c_courseTemplateExperimentId],
        config.c_fileName: values[config.c_fileName],
    }
    print(values)

    r = requests.delete(url, data=values)
    if r.status_code.__str__() != "200":
        logger.error("Post Experiment failed: request status not health: " + r.headers.__str__())
        return config.request_failed
    return config.request_success
