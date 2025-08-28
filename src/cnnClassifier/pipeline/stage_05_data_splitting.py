from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.utils.data_splitter import split_data
from cnnClassifier import logger

STAGE_NAME = "Data Splitting"

class DataSplittingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_splitting_config = config.get_data_splitting_config()
        split_data(
            source_dir=data_splitting_config.source_data_dir,
            dest_dir=data_splitting_config.root_dir
        )

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataSplittingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
