import great_expectations as ge
import pandas as pd
import datetime
import base64
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint
import os
from ruamel import yaml
import ruamel
import IPython
import streamlit as st
import streamlit.components.v1 as components

class DataQuality():

    def __init__(self, datasource_name, dataframe):
        """ 
        create great expectations context and default runtime datasource
        """
        self.datasource_name = datasource_name
        self.expectation_suite_name = f"{datasource_name}_expectation_suite"
        self.checkpoint_name = f"{datasource_name}_checkpoint"
        self.dataframe = dataframe
        self.partition_date = datetime.datetime.now()
        self.context = ge.get_context()

    def add_or_update_datasource(self):
        """
        Create data source if it does not exist or updating existing one
        """
        datasource_yaml = rf"""
        name: {self.datasource_name}
        class_name: Datasource
        execution_engine:
            class_name: PandasExecutionEngine
        data_connectors:
            runtime_connector:
                class_name: RuntimeDataConnector
                batch_identifiers:
                    - run_id
        """
        self.context.test_yaml_config(datasource_yaml)
        self.context.add_datasource(**yaml.load(datasource_yaml, Loader=ruamel.yaml.Loader))
    
    def add_or_update_datasource_2(self):
        datasource = self.context.sources.add_or_update_pandas(name=self.datasource_name)
        return datasource
    
    def create_data_asset(self):
        datasource = self.add_or_update_datasource_2()
        asset_name = f"{self.datasource_name}_{self.partition_date.date()}"
        data_asset = datasource.add_dataframe_asset(name=asset_name, dataframe=self.dataframe)
        return data_asset
    
    def get_batch_resquest(self):
        asset_name = self.create_data_asset()
        batch_request = asset_name.build_batch_request()
        return batch_request
    
    def get_validator_2(self):
        """
        Retrieve a validator object for a fine grain adjustment on the expectation suite.
        """
        batch_request = self.get_batch_resquest()
        self.add_or_update_ge_suite()
        validator = self.context.get_validator(batch_request=batch_request,
                                               expectation_suite_name=self.expectation_suite_name,
                                        )
        return validator

    def add_checkpoint_2(self):
        batch_request = self.get_batch_resquest()
        checkpoint = SimpleCheckpoint(
            name=self.checkpoint_name,
            data_context=self.context,
            validations=[
                {
                    "batch_request": batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )
        self.context.add_or_update_checkpoint(checkpoint=checkpoint)
        return checkpoint
    
    def run_checkpoint(self, checkpoint):
        checkpoint_result = checkpoint.run()
        return checkpoint_result
    
    def run_checks(self, expectation):
        """
        Run your dataquality checks here
        """
        validator = self.get_validator_2()
        def my_function(expectation, validator):
            local_vars = {"validator": validator}
            exec(f"expectation_result = validator.{expectation}", globals(), local_vars)
            return local_vars.get("expectation_result")
        
        expectation_result = my_function(expectation, validator)


        validator.save_expectation_suite(discard_failed_expectations=False)
        checkpoint = self.add_checkpoint_2()
        self.run_checkpoint(checkpoint)
        return expectation_result

    def configure_datasource(self):
        """
        Add a RuntimeDataConnector hat uses an in-memory DataFrame to a Datasource configuration
        """
        batch_request = RuntimeBatchRequest(
            datasource_name= self.datasource_name,
            data_connector_name= "runtime_connector",
            data_asset_name=f"{self.datasource_name}_{self.partition_date.strftime('%Y%m%d')}",
            batch_identifiers={
                "run_id": f'''
                {self.datasource_name}_partition_date={self.partition_date.strftime('%Y%m%d')}
                ''',
            },
            runtime_parameters={"batch_data": self.dataframe}
        )
        return batch_request
    
    def add_or_update_ge_suite(self):
        """
        create expectation suite if not exist and update it if there is already a suite
        """
        self.context.add_or_update_expectation_suite(
                     expectation_suite_name = self.expectation_suite_name)

    def get_validator(self):
        """
        Retrieve a validator object for a fine grain adjustment on the expectation suite.
        """
        self.add_or_update_datasource()
        batch_request = self.configure_datasource()
        self.add_or_update_ge_suite()
        validator = self.context.get_validator(batch_request=batch_request,
                                               expectation_suite_name=self.expectation_suite_name,
                                        )
        return validator, batch_request
    
    def run_expectation(self, expectation):
        """
        Run your dataquality checks here
        """
        validator, batch_request = self.get_validator()

        exec(f"expectation_result = validator.{expectation}")

        validator.save_expectation_suite(discard_failed_expectations=False)
        self.run_ge_checkpoint(batch_request)
    
    def add_or_update_ge_checkpoint(self):
        """
        Create new GE checkpoint or update an existing one
        """
        checkpoint_config = {
                    "name": self.checkpoint_name,
                    "class_name": "SimpleCheckpoint",
                    "run_name_template": "%Y%m%d-%H%M%S",
                }
        self.context.test_yaml_config(yaml.dump(checkpoint_config))
        self.context.add_or_update_checkpoint(**checkpoint_config)

    def run_ge_checkpoint(self, batch_request):
        """
        Run GE checkpoint
        """
        self.add_or_update_ge_checkpoint()

        self.context.run_checkpoint(
                checkpoint_name = self.checkpoint_name,
                validations=[
                            {
                             "batch_request": batch_request,
                            "expectation_suite_name": self.expectation_suite_name,
                            }
                            ],
                )
    def get_data_docs(self):
        """
        Define the button to open the HTML file
        """
        if st.button('Open Data Docs'):
            # Generate Data Docs
            self.context.open_data_docs()

            # Get the URL to the Data Docs
            data_docs_url = self.context.get_docs_sites_urls()[0]['site_url']

            # Display the link to the Data Docs
            st.markdown(f"Click [here]({data_docs_url}) to open the Data Docs.")
