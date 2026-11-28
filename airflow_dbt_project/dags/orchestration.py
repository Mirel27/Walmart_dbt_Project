from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator
from utills import trigger_databricks_job
from pendulum import datetime

@dag(
    dag_id="orchestration_dag",
    schedule="0 14 * * *",
    start_date=datetime(2026, 11, 28, tz="UTC"),
    catchup=False #For backfilling, set to True. For production, set to False
)
def orchestration():

    @task
    def ingest_cdc():
        print("Ingesting CDC data in Databricks...")
        trigger_databricks_job()

    # @task.bash
    # def cleanup():
    #     return " rm -rf /opt/airflow/walmart_project/target"

    source_freshness = BashOperator(
        task_id="source_freshness",
        bash_command="cd /opt/airflow/walmart_project && dbt source freshness --profiles-dir /opt/airflow/walmart_project"
    )

    silver_technical =  BashOperator(
        task_id="silver_technical",
        bash_command="cd /opt/airflow/walmart_project && dbt run --models silver_technical"
    )

    silver_ttechnical_t = BashOperator(
        task_id="silver_technical_t",
        bash_command="cd /opt/airflow/walmart_project && dbt test --models silver_technical"
    )

    silver_business = BashOperator(
        task_id="silver_business",
        bash_command="cd /opt/airflow/walmart_project && dbt run --models silver_business"
    )

    silver_business_t = BashOperator(
        task_id="silver_business_t",
        bash_command="cd /opt/airflow/walmart_project && dbt test --models silver_business"
    )

    gold_ephemeral = BashOperator(
        task_id="gold_ephemeral",
        cwd = "/opt/airflow/walmart_project",
        bash_command="dbt run --models gold_ephemeral"
    )

    gold_dimensional = BashOperator(
        task_id="gold_dimensional",
        cwd = "/opt/airflow/walmart_project",
        bash_command="dbt run -s snapshots"
    )

    gold_fact = BashOperator(
        task_id="gold_fact",
        cwd = "/opt/airflow/walmart_project",
        bash_command="dbt run --models gold_fact"
    )

    ingest_cdc()  >> source_freshness >> silver_technical >> silver_ttechnical_t >> silver_business >> silver_business_t >> gold_ephemeral >> gold_dimensional >> gold_fact     

orchestrate_dag = orchestration()