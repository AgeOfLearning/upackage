import os
import uuid
import time
import yaml
import tempfile
import tarfile
import logging
import re
from shutil import copyfile
from shutil import rmtree

DEFAULT_UNITY_ROOT_PATH = "Assets/"

class UPackage:
    metafile_template_path = "metafile_template.yaml"
    file_name_no_extension_pattern = "(.*)\..*$"

    @staticmethod
    def preprocess_assets(assets_root):
        UPackage._preprocess_files_in_path(assets_root)

    @staticmethod
    def _preprocess_files_in_path(asset_path):
        logging.info("Process files in directory: {0}".format(asset_path))

        # Process root folder...
        UPackage._process_file(asset_path)

        # Process contents...
        for path in os.listdir(asset_path):
            full_path = os.path.join(asset_path, path)

            if os.path.isdir(full_path):
                UPackage._process_file(full_path)
                UPackage._preprocess_files_in_path(full_path)

            if os.path.isfile(full_path):
                if full_path.endswith(".meta"):
                    continue
                else:
                    UPackage._process_file(full_path)

    @staticmethod
    def _get_file_path_no_extensions(file_path):
        match = re.search(UPackage.file_name_no_extension_pattern, file_path)
        return match.group(1)

    @staticmethod
    def _get_asset_meta_path(file_path):
        return "{0}.meta".format(file_path)

    @staticmethod
    def _process_file(file_path):
        logging.info("Processing file: {0}".format(file_path))
        meta_file_path = UPackage._get_asset_meta_path(file_path)

        if not os.path.isfile(meta_file_path):
            UPackage._generate_meta_file(meta_file_path)

    @staticmethod
    def _generate_meta_file(meta_file_path):
        logging.info("Generate meta file at: {0}".format(meta_file_path))

        with open(UPackage._get_metafile_template_path()) as file:
            contents = file.read()
            contents = contents.replace("{guid}", str(uuid.uuid4()).replace('-', ''))
            contents = contents.replace("{timeCreated}", str(int(time.time())))

            with open(meta_file_path, "w") as write_file_handle:
                write_file_handle.write(contents)

    @staticmethod
    def _get_metafile_template_path():
        sd = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(sd, UPackage.metafile_template_path)

    @staticmethod
    def _get_asset_root_basename(assets_root):
        return os.path.basename(assets_root)

    @staticmethod
    def generate_package(assets_root, output_path, unity_root_path=DEFAULT_UNITY_ROOT_PATH):
        tmpdir = tempfile.mkdtemp()
        assets = UPackage._collect_assets_in_path(assets_root)
        local_basename = UPackage._get_asset_root_basename(assets_root)
        temp_tar_path = os.path.join(tmpdir, "archtemp.tar")

        with tarfile.open(temp_tar_path, "w:gz") as tar:
            for asset in assets:
                asset_dir = os.path.join(tmpdir, asset['guid'])
                asset_path = os.path.join(asset_dir, 'asset')
                meta_path = os.path.join(asset_dir, 'asset.meta')
                path_name_path = os.path.join(asset_dir, 'pathname')
                path_name_local = asset['path'].replace(assets_root, "")

                if path_name_local.startswith(os.path.sep):
                    path_name_local = path_name_local.lstrip(os.path.sep)

                # replace root path with unity relative to Assets/...
                path_name_local = os.path.join(DEFAULT_UNITY_ROOT_PATH, local_basename, path_name_local)
                path_name_local = path_name_local.replace("\\", "/")

                if os.path.isdir(asset_dir):
                    rmtree(asset_dir)

                os.mkdir(asset_dir)

                if not os.path.isdir(asset['path']):
                    # copy asset...
                    copyfile(asset['path'], asset_path)

                # copy meta...
                copyfile(asset['meta_path'], meta_path)

                # write path name...
                with open(path_name_path, 'w') as write_file_handle:
                    write_file_handle.write(path_name_local)

                tar.add(asset_dir, arcname=asset['guid'])

        # Windows unity expects archtemp.tar inside of *.unitypackage
        copyfile(temp_tar_path, output_path)


    @staticmethod
    def _collect_assets_in_path(asset_path):
        assets = []

        asset_ref = UPackage._fetch_asset_reference(asset_path)
        if asset_ref is not None:
            logging.info("Adding asset ref: {0}".format(asset_ref))
            assets.append(asset_ref)

        for path in os.listdir(asset_path):
            full_path = os.path.join(asset_path, path)

            if os.path.isfile(full_path):
                asset_ref = UPackage._fetch_asset_reference(full_path)
                if asset_ref is not None:
                    logging.info("Adding asset ref: {0}".format(asset_ref))
                    assets.append(asset_ref)

            if os.path.isdir(full_path):
                sub_assets = UPackage._collect_assets_in_path(full_path)
                for sub_asset in sub_assets:
                    assets.append(sub_asset)

        return assets

    @staticmethod
    def _fetch_asset_reference(file_path):
        meta_file_path = UPackage._get_asset_meta_path(file_path)

        if os.path.isfile(meta_file_path):
            with open(meta_file_path) as meta_file_stream:
                try:
                    meta_file = yaml.load(meta_file_stream)
                    return {
                        'guid': meta_file['guid'],
                        'path': file_path,
                        'meta_path': meta_file_path
                    }
                except yaml.YAMLError as exc:
                    print(exc)
