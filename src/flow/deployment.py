from src.flow.pipeline import etl_pipeline
from prefect.server.schemas.schedules import CronSchedule

if __name__ == "__main__":
    etl_pipeline.deploy(
        name="BRFSS-Yearly",
        schedule=CronSchedule(cron="0 0 1 1 *", timezone="Asia/Jakarta"),
        work_pool_name="default",
        tags=["brfss", "diabetes", "etl"]
    )
