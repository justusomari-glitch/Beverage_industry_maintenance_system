from base_consumer import run
from config import TOPICS

if __name__ == "__main__":
    run(
        topic=TOPICS['Production Line'],
        group_id="production-line-consumer-group",
        table_name="production_line_predictions"
    )