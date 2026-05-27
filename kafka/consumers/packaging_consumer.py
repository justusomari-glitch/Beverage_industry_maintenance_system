from base_consumer import run
from config import TOPICS

if __name__ == "__main__":
    run(
        topic=TOPICS['Packaging'],
        group_id="packaging-consumer-group",
        table_name="packaging_predictions"
    )