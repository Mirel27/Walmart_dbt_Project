from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    schedule=None,
    catchup=False
)
def orchestration():

    @task
    def ingest_cdc():
        print("Ingesting CDC data in Databricks...")

    source_freshness = BashOperator(
        task_id="source_freshness",
        bash_command="cd /opt/airflow/walmart_project && dbt source freshness"
    )

    ingest_cdc() >> source_freshness

orchestrate_dag = orchestration()