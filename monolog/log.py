import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from imageio import imwrite

# constants
_ROOT = os.path.abspath(os.path.dirname(__file__))

# -----------------------------
# Experiment object
# -----------------------------


class Experiment(object):
    def __init__(
        self,
        name='default',
        debug=False,
        version=None,
        save_dir=None,
        autosave=True,
        description=None,
        create_git_tag=False,
    ):
        """
        A new Experiment object defaults to 'default' unless a specific name is provided
        If a known name is already provided, then the file version is changed
        :param name:
        :param debug:
        """
        # change where the save dir is if requested
        if save_dir is not None:
            global _ROOT
            _ROOT = save_dir

        self.metrics = []
        self.tags = {}
        self.name = name
        self.debug = debug
        self.version = version
        self.autosave = autosave
        self.description = description
        self.create_git_tag = create_git_tag
        self.exp_hash = '{}_v{}'.format(self.name, version)
        self.created_at = str(datetime.utcnow())

        # update version hash if we need to increase version on our own
        # we will increase the previous version, so do it now so the hash
        # is accurate
        if version is None:
            old_version = self.__get_last_experiment_version()
            self.exp_hash = '{}_v{}'.format(self.name, old_version + 1)
            self.version = old_version + 1

        self.__init_cache_file_if_needed()

        # create a new log file if not in debug mode
        if not debug:

            # when we have a version, load it
            if self.version is not None:

                # when no version and no file, create it
                if not os.path.exists(self.__get_log_name()):
                    self.__create_exp_file(self.version)
                    self.save()
                else:
                    # otherwise load it
                    self.__load()
            else:
                # if no version given, increase the version to a new exp
                # create the file if not exists
                old_version = self.__get_last_experiment_version()
                self.version = old_version
                self.__create_exp_file(self.version + 1)
                self.save()

            # create a git tag if requested
            if self.create_git_tag == True:
                desc = description if description is not None else 'no description'
                tag_msg = 'Test tube exp: {} - {}'.format(self.name, desc)
                cmd = 'git tag -a tt_{} -m "{}"'.format(self.exp_hash, tag_msg)
                os.system(cmd)
                print('Test tube created git tag:', 'tt_{}'.format(self.exp_hash))

    def argparse(self, argparser):
        parsed = vars(argparser)
        to_add = {}

        # don't store methods
        for k, v in parsed.items():
            if not callable(v):
                to_add[k] = v

        self.tag(to_add)

    def add_meta_from_hyperopt(self, hypo):
        """
        Transfers meta data about all the params from the
        hyperoptimizer to the log
        :param hypo:
        :return:
        """
        meta = hypo.get_current_trial_meta()
        for tag in meta:
            self.tag(tag)

    # --------------------------------
    # FILE IO UTILS
    # --------------------------------
    def __init_cache_file_if_needed(self):
        """
        Inits a file that we log historical experiments
        :return:
        """
        exp_cache_file = self.get_data_path(self.name, self.version)
        if not os.path.isdir(exp_cache_file):
            os.makedirs(exp_cache_file)

    def __create_exp_file(self, version):
        """
        Recreates the old file with this exp and version
        :param version:
        :return:
        """
        exp_cache_file = self.get_data_path(self.name, self.version)
        # if no exp, then make it
        path = '{}/meta.experiment'.format(exp_cache_file)
        open(path, 'w').close()
        self.version = version

        # make the directory for the experiment media assets name
        os.mkdir(self.get_media_path(self.name, self.version))

    def __get_last_experiment_version(self):
        try:
            exp_cache_file = os.sep.join(self.get_data_path(self.name, self.version).split(os.sep)[:-1])
            last_version = -1
            for f in os.listdir(exp_cache_file):
                if 'version_' in f:
                    file_parts = f.split('_')
                    version = int(file_parts[-1])
                    last_version = max(last_version, version)
            return last_version
        except Exception as e:
            return -1

    def __get_log_name(self):
        exp_cache_file = self.get_data_path(self.name, self.version)
        return '{}/meta.experiment'.format(exp_cache_file)

    def tag(self, tag_dict):
        """
        Adds a tag to the experiment.
        Tags are metadata for the exp.

        >> e.tag({"model": "Convnet A"})

        :param key:
        :param val:
        :return:
        """
        if self.debug: return

        # parse tags
        for k, v in tag_dict.items():
            self.tags[k] = v

        # save if needed
        if self.autosave == True:
            self.save()

    def log(self, metrics_dict):
        """
        Adds a json dict of metrics.

        >> e.log({"loss": 23, "coeff_a": 0.2})

        :param metrics_dict:
        :return:
        """
        if self.debug: return

        # timestamp
        if 'created_at' not in metrics_dict:
            metrics_dict['created_at'] = str(datetime.utcnow())

        self.__convert_numpy_types(metrics_dict)
        self.metrics.append(metrics_dict)
        if self.autosave == True:
            self.save()

    def __convert_numpy_types(self, metrics_dict):
        for k, v in metrics_dict.items():
            if v.__class__.__name__ == 'float32':
                metrics_dict[k] = float(v)

            if v.__class__.__name__ == 'float64':
                metrics_dict[k] = float(v)

    def save(self):
        """
        Saves current experiment progress
        :return:
        """
        if self.debug: return

        # save images and replace the image array with the
        # file name
        self.__save_images(self.metrics)
        metrics_file_path = self.get_data_path(self.name, self.version) + '/metrics.csv'
        meta_tags_path = self.get_data_path(self.name, self.version) + '/meta_tags.csv'

        obj = {
            'name': self.name,
            'version': self.version,
            'tags_path': meta_tags_path,
            'metrics_path': metrics_file_path,
            'autosave': self.autosave,
            'description': self.description,
            'created_at': self.created_at,
            'exp_hash': self.exp_hash
        }

        # save the experiment meta file
        with open(self.__get_log_name(), 'w') as file:
            json.dump(obj, file, ensure_ascii=False)

        # save the metatags file
        df = pd.DataFrame({'key': list(self.tags.keys()), 'value': list(self.tags.values())})
        df.to_csv(meta_tags_path, index=False)

        # save the metrics data
        df = pd.DataFrame(self.metrics)
        df.to_csv(metrics_file_path, index=False)

    def __save_images(self, metrics):
        """
        Save tags that have a png_ prefix (as images)
        and replace the meta tag with the file name
        :param metrics:
        :return:
        """
        # iterate all metrics and find keys with a specific prefix
        for i, metric in enumerate(metrics):
            for k, v in metric.items():
                # if the prefix is a png, save the image and replace the value with the path
                img_extension = None
                img_extension = 'png' if 'png_' in k else img_extension
                img_extension = 'jpg' if 'jpg' in k else img_extension
                img_extension = 'jpeg' if 'jpeg' in k else img_extension

                if img_extension is not None:
                    # determine the file name
                    img_name = '_'.join(k.split('_')[1:])
                    save_path = self.get_media_path(self.name, self.version)
                    save_path = '{}/{}_{}.{}'.format(save_path, img_name, i, img_extension)

                    # save image to disk
                    if type(metric[k]) is not str:
                        imwrite(save_path, metric[k])

                    # replace the image in the metric with the file path
                    metric[k] = save_path

    def __load(self):
        # load .experiment file
        with open(self.__get_log_name(), 'r') as file:
            data = json.load(file)
            self.name = data['name']
            self.version = data['version']
            self.autosave = data['autosave']
            self.created_at = data['created_at']
            self.description = data['description']
            self.exp_hash = data['exp_hash']

        # load .tags file
        meta_tags_path = self.get_data_path(self.name, self.version) + '/meta_tags.csv'
        df = pd.read_csv(meta_tags_path)
        self.tags_list = df.to_dict(orient='records')
        self.tags = {}
        for d in self.tags_list:
            k, v = d['key'], d['value']
            self.tags[k] = v

        # load metrics
        metrics_file_path = self.get_data_path(self.name, self.version) + '/metrics.csv'
        try:
            df = pd.read_csv(metrics_file_path)
            self.metrics = df.to_dict(orient='records')

            # remove nans
            for metric in self.metrics:
                to_delete = []
                for k, v in metric.items():
                    try:
                        if np.isnan(v):
                            to_delete.append(k)
                    except Exception as e:
                        pass

                for k in to_delete:
                    del metric[k]
        except Exception as e:
            # metrics was empty...
            self.metrics = []

    def get_data_path(self, exp_name, exp_version):
        """
        Returns the path to the local package cache
        :param path:
        :return:
        """
        return os.path.join(_ROOT, exp_name, 'version_{}'.format(exp_version))

    def get_media_path(self, exp_name, exp_version):
        """
        Returns the path to the local package cache
        :param path:
        :return:
        """
        return os.path.join(self.get_data_path(exp_name, exp_version), 'media')

    # ----------------------------
    # OVERWRITES
    # ----------------------------

    def __str__(self):
        return 'Exp: {}, v: {}'.format(self.name, self.version)

    def __hash__(self):
        return 'Exp: {}, v: {}'.format(self.name, self.version)
