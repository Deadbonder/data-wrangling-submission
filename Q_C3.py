
from airflow.sdk import dag, task


@dag(dag_id="stock_check", schedule=None)
def stock_check():

    @task.python
    def check_stock():
        return {'item': "rice", 'qty': 12}

    # returns the task_id of the path to follow
    @task.branch
    def decide(stock):
        if stock['qty'] < 20:
            return "place_order"
        return "skip_order"

    @task.bash
    def place_order():
        return 'echo "Stock is low, placing order"'

    @task.bash
    def skip_order():
        return 'echo "Stock is enough, skipping order"'

    # default trigger rule (all_success) would skip notify because one branch is always skipped, so run it as long as nothing failed
    @task.python(trigger_rule="none_failed_min_one_success")
    def notify():
        print("Stock check done")

    decide(check_stock()) >> [place_order(), skip_order()] >> notify()


stock_check()

# DAG:
#
#                                -------------
#                            --> | place_order | --+
#  -------------     --------    -------------     |  --------
# | check_stock |-->| decide |                   --> | notify |
#  -------------      -------    -------------     |  --------
#                            --> | skip_order  | --+
#                                 -------------
#
# For qty = 12: 12 < 20, so decide returns "place_order".
# place_order runs, skip_order is SKIPPED, notify still runs.
