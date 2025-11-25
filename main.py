import os
from concurrent.futures import ProcessPoolExecutor
from . import config
from scrapper.crawler import crawl
from scrapper.parser import run_parser

def run_pipeline_worker(project_name):
    """
    Worker function executed in a separate process.
    """
    # Get Process ID to track different workers
    worker_id = os.getpid()
    
    try:
        #  STEP 1: CRAWLER 
        raw_html = crawl(project_name)

        if not raw_html:
            return

       #STEP 2: PARSER 
        run_parser(project_name)

    except Exception as e:
        print(f"[Worker-{worker_id}] [CRITICAL FAILURE] {str(e)}")

def main():
    # 1. Define the list of projects to run
    PROJECT_LIST = ["meesho", "linkedin"]

    # 2. Configure Worker Pool
    # Limit max_workers to avoid freezing the CPU (e.g., max 4 browsers at once)
    num_workers = min(len(PROJECT_LIST), 4)

    # 3. Launch Processes
    # 'map' will distribute the items in PROJECT_LIST to available workers
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        executor.map(run_pipeline_worker, PROJECT_LIST)

    print(" All jobs execution completed ")

if __name__ == "__main__":
    main()