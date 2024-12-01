import time
import threading

from Backend.GlobalController.Instance import Instance
factor_milliseconds_to_seconds = 1000
cond = threading.Condition()
stop_event = threading.Event()
current_start_activity = 0


def stop_processing():
    with cond:
        stop_event.set()
    print("stop processing")


def start_processing_again(new_activity_id=None):
    global current_start_activity
    # Before notifying the condition, wait for the about_to_wait_event to ensure that continue_running() is waiting
    with cond:
        if new_activity_id is not None:
            current_start_activity = new_activity_id
        stop_event.clear()
        cond.notify()


def load_instance_replay(assistance, db, instance_id,  user_name=None, user_id=None):
    # TODO check that nothing changes

    # load data from database
    assistance.use_clevr = True

    assistance.instance = Instance(assistance.user, assistance.library,

                                   reference_model=assistance.model,
                                   activities=[],
                                   id=-1)
    seq = 0

    query = {"id": user_id}
    user = db['user'].find_one(query)

    for entry in user['history']:
        if entry['UUID'] == instance_id:
            instance = entry

    nodes_act_id = list(instance['nodes'].keys())
    nodes_values = list(instance['nodes'].values())

    currenty_start_activity = 0
    print("lets start")
    return nodes_act_id, nodes_values, current_start_activity


def replay_page(assistance, nodes_id, nodes_values, currenty_start_activity, sleep=True):
    threading.Thread(target=continue_running, args=(
        nodes_id, nodes_values, current_start_activity, assistance, sleep)).start()


def continue_running(nodes_ids, nodes_values, current_start_activity, assistance, sleep):

    left_to_run = nodes_ids[current_start_activity:]

    for item in left_to_run:
        activity = nodes_values[current_start_activity]
        duration = int(activity['duration']) if activity else 0

        # If stop_event is set, wait until it's cleared to continue
        with cond:
            while stop_event.is_set():
                cond.wait()

        add = {'Activity': [{'BPMNObject': [{'ObjectId': item}]}, {'Sequence': str(current_start_activity)},
                            {'CalledForHelp': 'false'}, {
                            'StartDate': '2022-01-27T22:37:54.213Z'},
                            {'Duration': str(duration)}]}
        current_start_activity += 1
        print(activity)

        assistance.activities = [add]
        assistance.assist_status = assistance.update(no_test=False)

      #  print( assistance.assist_status)
        if sleep:
            time.sleep(duration / factor_milliseconds_to_seconds)
