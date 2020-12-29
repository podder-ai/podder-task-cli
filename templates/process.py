from pathlib import Path

from podder_task_foundation import Context, Payload
from podder_task_foundation import Process as ProcessBase


class Process(ProcessBase):
    def initialize(self, context: Context) -> None:
        # Initialization need to be done here
        # Never do the initialization on execute method !
        # - Model loading
        # - Large text(json) file loading
        # - Prepare some data
        self._model_file_path = Path(
            context.file.get_data_file(context.config.get("model.name")))

    def execute(self, input_payload: Payload, output_payload: Payload,
                context: Context):
        # Get Input
        # input_image = input_payload.get_image()  # Get Pillow Image from input
        # Get input data {{ input_code }}

        # Do something
        result = {}
        context.logger.info("some message")

        # Output result {{ output_code }}

