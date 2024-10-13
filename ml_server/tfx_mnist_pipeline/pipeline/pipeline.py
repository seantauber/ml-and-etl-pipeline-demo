import os
from tfx.orchestration import metadata
from tfx.orchestration.local import local_dag_runner
from . import components

def run():
    pipeline_name = 'mnist_pipeline'
    pipeline_root = os.path.join('/app', 'tfx_pipelines', pipeline_name)
    data_root = os.path.join('/app', 'data')
    serving_model_dir = os.path.join('/app', 'serving_model', pipeline_name)

    components_list = components.create_pipeline(
        pipeline_root=pipeline_root,
        data_root=data_root,
        serving_model_dir=serving_model_dir,
    )

    metadata_config = metadata.sqlite_metadata_connection_config(
        os.path.join(pipeline_root, 'metadata.sqlite')
    )

    local_dag_runner.LocalDagRunner().run(
        pipeline_definitions.create_pipeline(
            pipeline_name=pipeline_name,
            pipeline_root=pipeline_root,
            components=components_list,
            metadata_connection_config=metadata_config,
        )
    )
