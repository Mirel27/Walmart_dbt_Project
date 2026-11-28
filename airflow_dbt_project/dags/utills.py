import os
import time
from pathlib import Path

from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState,RunResultState


def trigger_databricks_job() -> None:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")
    if not host or not token:
        raise RuntimeError("DATABRICKS_HOST and DATABRICKS_TOKEN must be set in the repository-root .env file")

    workspace = WorkspaceClient(host=host, token=token)
    job_trigger = workspace.jobs.run_now(job_id="340476672004559")

    while True:
        job_status = workspace.jobs.get_run(run_id=job_trigger.run_id)
        print(f"Job status: {job_status.state.life_cycle_state}, Result state: {job_status.state.result_state}")
        if job_status.state.life_cycle_state in [
            RunLifeCycleState.TERMINATED,
            RunLifeCycleState.SKIPPED,
            RunLifeCycleState.INTERNAL_ERROR,
        ]:
            if job_status.state.result_state != RunResultState.SUCCESS:
                raise RuntimeError(f"Job failed with state: {job_status.state.result_state}")
            print("Job completed successfully.")
            break

        time.sleep(10)

    print(f"Triggered job with run_id: {job_trigger.run_id}")