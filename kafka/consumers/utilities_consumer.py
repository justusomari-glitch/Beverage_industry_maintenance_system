from base_consumer import run
from config import TOPICS

if __name__ == "__main__":
    run(
        topic=TOPICS['Utilities'],
        group_id="utilities-consumer-group",
        table_name="utilities_predictions"
    )