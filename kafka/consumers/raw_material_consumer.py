from base_consumer import run
from config import TOPICS

if __name__ == "__main__":
    run(
        topic=TOPICS['Raw Material Processing'],
        group_id="raw-materials-consumer-group",
        table_name="raw_material_predictions"
    )