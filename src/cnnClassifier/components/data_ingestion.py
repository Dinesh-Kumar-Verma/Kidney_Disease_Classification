import os
import zipfile
import kaggle
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        '''
        Fetch data from Kaggle
        '''
        try:
            dataset_name = self.config.source_URL
            zip_download_dir = os.path.dirname(self.config.local_data_file)
            os.makedirs(zip_download_dir, exist_ok=True)
            logger.info(f"Downloading data from Kaggle dataset {dataset_name} into file {self.config.local_data_file}")

            # Authenticate with Kaggle API
            kaggle.api.authenticate()

            # Download the dataset
            kaggle.api.dataset_download_files(dataset_name, path=zip_download_dir, unzip=False)
            
            # Rename the downloaded file
            downloaded_file_name = dataset_name.split('/')[1] + '.zip'
            os.rename(os.path.join(zip_download_dir, downloaded_file_name), self.config.local_data_file)

            logger.info(f"Downloaded data from {dataset_name} into file {self.config.local_data_file}")

        except Exception as e:
            logger.exception(e)
            raise e

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)