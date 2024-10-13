import os
from tfx.components import (
    ImportExampleGen,
    Trainer,
    Evaluator,
    Pusher,
)
from tfx.proto import trainer_pb2, pusher_pb2
from tfx.dsl.components.base import executor_spec
from tfx.components.trainer.executor import GenericExecutor

def create_pipeline(pipeline_root, data_root, serving_model_dir):
    # ExampleGen: Import data
    example_gen = ImportExampleGen(input_base=data_root)

    # Trainer: Train the model
    trainer = Trainer(
        module_file=os.path.join(os.getcwd(), 'pipeline', 'model.py'),
        examples=example_gen.outputs['examples'],
        train_args=trainer_pb2.TrainArgs(num_steps=2000),
        eval_args=trainer_pb2.EvalArgs(num_steps=500),
        custom_executor_spec=executor_spec.ExecutorClassSpec(GenericExecutor),
    )

    # Evaluator: Evaluate the model
    evaluator = Evaluator(
        examples=example_gen.outputs['examples'],
        model=trainer.outputs['model'],
    )

    # Pusher: Deploy the model
    pusher = Pusher(
        model=trainer.outputs['model'],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=serving_model_dir
            )
        ),
    )

    return [
        example_gen,
        trainer,
        evaluator,
        pusher,
    ]
