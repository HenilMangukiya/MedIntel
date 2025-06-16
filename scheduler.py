from apscheduler.schedulers.blocking import BlockingScheduler
import ingestion.openfda_ingest as openfda
import ingestion.covid_ingest as covid

def run_all_jobs():
    print("🔁 Running all ingestion jobs...")
    openfda.fetch_and_store_data()
    covid.fetch_and_store_covid_data()
    print("✅ All jobs done.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Run every 5 minutes
    scheduler.add_job(run_all_jobs, 'interval', minutes=5)

    print("🚀 Scheduler started. Data will update every 5 minutes.")
    run_all_jobs()  # Run once immediately
    scheduler.start()
