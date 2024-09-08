import json
import os
from pathlib import Path
import sys
import tempfile
from kfp import compiler, dsl
import google.cloud.aiplatform as aip


STAGING_BUCKET = f'gs://{os.environ["STAGING_BUCKET"]}'


if __name__ == "__main__":
    service_account = json.load(open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])).get("client_email")
    template_path = tempfile.mkstemp(suffix=".yaml")[1]

    if sys.argv[0] == "workflow":
        pass
    else: # create a pipeline comprising only the specified container & arguments
        @dsl.container_component
        def container_component():
            return dsl.ContainerSpec(
                image=sys.argv[1],
                args=sys.argv[2:]
            )

        @dsl.pipeline
        def pipeline():
            container_component()


    compiler.Compiler().compile(
        pipeline_func = pipeline,
        package_path = template_path
    )

    # Submit job to Vertex AI
    aip.init(staging_bucket=STAGING_BUCKET)

    job = aip.PipelineJob(
        display_name=sys.argv[1],
        template_path=template_path,
        enable_caching=False,
    )

    job.run(service_account=service_account)
