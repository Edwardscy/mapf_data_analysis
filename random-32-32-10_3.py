
import json
import os
import matplotlib.pyplot as plt
import matplotlib.transforms
import matplotlib
import numpy as np
import pathlib
import math
from matplotlib.widgets import TextBox

# base_folder = os.path.join(dir_path, './data_store/random-32-32-10/add_and_delete_obstacles')
# base_folder = os.path.join(dir_path, './data_store/random-32-32-10/only_delete_obstacles')
# base_folder = os.path.join(dir_path, './data_store/random-32-32-10/only_add_obstacles')
# test_name = "random-32-32-10 add_and_delete_obstacles"

scen_counts = 25 + 1
agent_max_counts = 30 + 2
agent_start_num = 4


data_folder_name = "random-32-32-10"
test_model = "add_and_delete_obstacles"
plot_mode = "runtime"

def get_test_model(mode):
    if mode == "only_add_obstacles":
        return "Scenario 1: Only add obstacles"
    elif mode == "only_delete_obstacles":
        return "Scenario 2: Only delete obstacles"
    elif mode == "add_and_delete_obstacles":
        return "Scenario 1: Add add delete obstacles"

xlabel_name = "Number of obstacle added_or_deleted"
ylabel_name = "runtime_diff / sec"


dir_path = os.path.dirname(os.path.realpath(__file__))
base_folder = os.path.join(dir_path, "./data_store/never_clear/")
base_folder = base_folder + "/" + data_folder_name + "/" + test_model

base_save_pic_name = data_folder_name + "_" + test_model

thesis_report_picture_folder = os.path.join(dir_path, "./thesis_report_picture/never_clear")
save_pic_folder = thesis_report_picture_folder + "/" + data_folder_name + "/" + test_model + "/" + plot_mode

CREATE_FOLDER_FLAG = True
if CREATE_FOLDER_FLAG:
    pathlib.Path(save_pic_folder).mkdir(parents=True, exist_ok=True)





data_dic = {}
data_dic["new_cbs"] = {}
data_dic["old_cbs"] = {}
for i in range(1, scen_counts, 1):
    scen_file_id = str(i)
    data_dic["new_cbs"][scen_file_id] = {}
    data_dic["old_cbs"][scen_file_id] = {}
    for j in range(4, agent_max_counts, 2):
        agent_num = str(j)
        if agent_num in ["20", "22", "26"]:
            continue

        data_dic["new_cbs"][scen_file_id][agent_num] = {}
        data_dic["old_cbs"][scen_file_id][agent_num] = {}

        new_cbs_result_file = base_folder + "/random-32-32-10-even-" + scen_file_id + "/" + agent_num + "/new_cbs_result.json"
        old_cbs_result_file = base_folder + "/random-32-32-10-even-" + scen_file_id + "/" + agent_num + "/old_cbs_result.json"

        with open(new_cbs_result_file, 'r') as f:
            data = json.load(f)

            for key, value in data.items():
                if key != "test_infos":
                    data_dic["new_cbs"][scen_file_id][agent_num][key] = {}
                    data_dic["new_cbs"][scen_file_id][agent_num][key]["result"] = value["result"]
                    data_dic["new_cbs"][scen_file_id][agent_num][key]["runtime"] = value["runtime"]

        try:
            with open(old_cbs_result_file, 'r') as f:
                data = json.load(f)

                for key, value in data.items():
                    if key != "test_infos":
                        data_dic["old_cbs"][scen_file_id][agent_num][key] = {}
                        data_dic["old_cbs"][scen_file_id][agent_num][key]["result"] = value["result"]
                        data_dic["old_cbs"][scen_file_id][agent_num][key]["runtime"] = value["runtime"]
        except Exception as e:
            print(e)
            with open(new_cbs_result_file, 'r') as f:
                data = json.load(f)

                for key, value in data.items():
                    if key != "test_infos":
                        data_dic["old_cbs"][scen_file_id][agent_num][key] = {}
                        data_dic["old_cbs"][scen_file_id][agent_num][key]["result"] = value["result"]
                        data_dic["old_cbs"][scen_file_id][agent_num][key]["runtime"] = value["runtime"]


success_rate_statistics = {}
for i in range(agent_start_num, agent_max_counts, 2):
    agent_num = str(i)
    if agent_num in ["20", "22", "26"]:
        continue

    success_rate_statistics[agent_num] = {}
    success_rate_statistics[agent_num]["new_cbs_fail"] = 0
    success_rate_statistics[agent_num]["old_cbs_fail"] = 0
    success_rate_statistics[agent_num]["total_count"] = 0

runtime_diff_max_dic = {}
for j in range(agent_start_num, agent_max_counts, 2):
    agent_num = str(j)
    runtime_diff_max_dic[agent_num] = 0

runtime_dic = {}
for i in range(1, scen_counts, 1):
    scen_file_id = str(i)
    runtime_dic[scen_file_id] = {}
    for j in range(agent_start_num, agent_max_counts, 2):
        agent_num = str(j)
        if agent_num in ["20", "22", "26"]:
            continue

        runtime_dic[scen_file_id][agent_num] = []
        for key in data_dic["new_cbs"][scen_file_id][agent_num].keys():

            new_cbs_result = data_dic["new_cbs"][scen_file_id][agent_num][key]["result"]
            new_cbs_runtime = data_dic["new_cbs"][scen_file_id][agent_num][key]["runtime"]

            old_cbs_result = data_dic["old_cbs"][scen_file_id][agent_num][key]["result"]
            old_cbs_runtime = data_dic["old_cbs"][scen_file_id][agent_num][key]["runtime"]

            if new_cbs_result == "Optimal" and old_cbs_result == "Optimal":
                runtime_diff = new_cbs_runtime - old_cbs_runtime

                # runtime_diff = (new_cbs_runtime + 0.0000001)/(old_cbs_runtime + 0.0000001)
                # runtime_diff = np.log10(runtime_diff)
                runtime_dic[scen_file_id][agent_num].append(runtime_diff)

                if abs(runtime_diff) > runtime_diff_max_dic[agent_num]:
                    runtime_diff_max_dic[agent_num] = abs(runtime_diff)

            elif new_cbs_result != "Optimal" and old_cbs_result == "Optimal":
                runtime_dic[scen_file_id][agent_num].append("new")
                print("new_cbs_result", scen_file_id, agent_num)
                success_rate_statistics[agent_num]["new_cbs_fail"] += 1
            elif new_cbs_result == "Optimal" and old_cbs_result != "Optimal":
                runtime_dic[scen_file_id][agent_num].append("old")
                print("old_cbs_result", scen_file_id, agent_num)
                success_rate_statistics[agent_num]["old_cbs_fail"] += 1
            elif new_cbs_result != "Optimal" and old_cbs_result != "Optimal":
                runtime_dic[scen_file_id][agent_num].append("all")
                success_rate_statistics[agent_num]["new_cbs_fail"] += 1
                success_rate_statistics[agent_num]["old_cbs_fail"] += 1
            success_rate_statistics[agent_num]["total_count"] += 1


for key, value in success_rate_statistics.items():
    print(key, value)



offset_value = 200
no_solution_dic = {}
for i in range(1, scen_counts, 1):
    scen_file_id = str(i)
    for j in range(agent_start_num, agent_max_counts, 2):
        agent_num = str(j)
        if agent_num in ["20", "22", "26"]:
            continue

        for k in range(len(runtime_dic[scen_file_id][agent_num])):

            key_str = str(k)
            if runtime_dic[scen_file_id][agent_num][k] == "new":
                runtime_dic[scen_file_id][agent_num][k] = 0 #runtime_diff_max + offset_value #data_dic["old_cbs"][scen_file_id][agent_num][key_str]["runtime"]
                no_solution_dic[(scen_file_id, agent_num, k)] = "new"
            elif runtime_dic[scen_file_id][agent_num][k] == "old":
                runtime_dic[scen_file_id][agent_num][k] = 0 #(-1)*(runtime_diff_max + offset_value)#data_dic["new_cbs"][scen_file_id][agent_num][key_str]["runtime"]
                no_solution_dic[(scen_file_id, agent_num, k)] = "old"
            elif runtime_dic[scen_file_id][agent_num][k] == "all":
                runtime_dic[scen_file_id][agent_num][k] = 0
                no_solution_dic[(scen_file_id, agent_num, k)] = "all"


# for key, value in no_solution_dic.items():
#     print(key, value)
#     print(runtime_dic[key[0]][key[1]][key[2]])


x_array = np.array([i for i in range(0, 10, 1)])

axv_line_arr = np.array([d*25 for d in range(11)])

# agent_start_num = agent_max_counts - 2

for i in range(agent_start_num, agent_max_counts, 2):
    agent_num = str(i)
    if agent_num in ["20", "22", "26"]:
        continue

    fig = plt.figure(figsize=(15, 8))
    ax = plt.axes()

    plt.yscale("symlog")

    dx = 36 / 72.
    dy = 0 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    print(offset)
    # apply offset transform to all x ticklabels.

    # print(plt.axis().get_majorticklabels())
    # print(plt.xticks())

    print(ax)
    for label in ax.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    # ax.set_xticks([0, np.pi, 2 * np.pi])
    # plt.xticks(["A","A","A","A","A","A","A","A","A","A"])
    # ["Jan\n2009", "Feb\n2009", "Mar\n2009", "Apr\n2009", "May\n2009"])
    #########################################

    for step in range(11):
        # plt.axvline(x=step * 25, color='r', label='axvline - full height')
        # plt.axvline(x=step * 25, color="orange", linestyle="--")
        plt.axvline(x=step * 5, color="orange", linestyle="--")

    runtime_diff_max = runtime_diff_max_dic[agent_num]

    plt.text(-9.6, runtime_diff_max+offset_value, 'Lifelong CBS Timeout', color="red")
    plt.text(-7, (-1)*(runtime_diff_max+offset_value), 'CBS Timeout', color="red")

    plt.axhline(y=runtime_diff_max + offset_value, color="g", linestyle="--")
    plt.axhline(y=0, color="g", linestyle="--")
    plt.axhline(y=(-1)*(runtime_diff_max + offset_value), color="g", linestyle="--")

    # plt.xticks([1,2,3])

    for step in range(10):
        x_array = np.array([d/5.0 for d in range(step*25, (step + 1)*25)])
        y_list = []
        for scen_id in range(1, 26, 1):
            scen_file_id = str(scen_id)
            y_list.append(runtime_dic[scen_file_id][agent_num][step])

            for key, value in no_solution_dic.items():
                # scen_file_id, agent_num, k
                if (scen_file_id == key[0]) and (agent_num == key[1]) and (step == key[2]):
                    x = step * 25 + scen_id
                    x = x / 5.0

                    if value == "all":
                        plt.scatter(x, runtime_dic[key[0]][key[1]][key[2]], marker="*", c="blue", s=200, alpha=0.5)
                    elif value == "new":
                        plt.scatter(x, runtime_diff_max + offset_value, marker="X", c="red", s=200, alpha=0.5)
                    elif value == "old":
                        plt.scatter(x, (-1)*(runtime_diff_max + offset_value), marker="X", c="red", s=200, alpha=0.5)

        y_array = np.array(y_list)

        # label = "add " + str(step*5) + " obstacles"
        # plt.scatter(x_array, y_array, marker="o", s=50, alpha=0.5, label=label)

        plt.scatter(x_array, y_array, marker="o", s=50, alpha=0.5)



        # plt.xticks(x_array)
        # ["Jan\n2009", "Feb\n2009", "Mar\n2009", "Apr\n2009", "May\n2009"])


    plt.legend(loc='lower right')

    new_cbs_success_count = success_rate_statistics[agent_num]["total_count"] - \
                             success_rate_statistics[agent_num]["new_cbs_fail"]
    old_cbs_success_count = success_rate_statistics[agent_num]["total_count"] - \
                             success_rate_statistics[agent_num]["old_cbs_fail"]
    total_count = success_rate_statistics[agent_num]["total_count"]

    new_cbs_success_rate = new_cbs_success_count/total_count
    old_cbs_success_rate = old_cbs_success_count / total_count

    save_pic_name = base_save_pic_name + " agent_num " + agent_num
    save_pic_name_path = save_pic_folder + "/" + save_pic_name + ".png"
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    result_infos = "Lifelong CBS success rate:" + str(new_cbs_success_rate) + "\n" + \
                    "CBS success rate: " + str(old_cbs_success_rate) + "\n" + \
                    "Lifelong CBS success count: " + str(new_cbs_success_count) + "\n" + \
                    "CBS success count: " + str(old_cbs_success_count) + "\n" + \
                    "Total count: " + str(total_count)

    title_name = "Map name: " + data_folder_name + "\n" + \
                 get_test_model(test_model) + "\n" + \
                 "Agent_num " + agent_num

    # plt.title(save_pic_name + "\n")
    plt.title(title_name)

    locs, labels = plt.xticks([d for d in range(0, 55, 5)], rotation=0)

    yticks = ax.yaxis.get_major_ticks()
    yticks[0].set_visible(False)
    yticks[6].set_visible(False)

    # print(locs)
    # print(labels)



    # text_box = TextBox(axbox, "Evaluate")
    # text_box.set_val("t ** 2")  # Trigger `submit` with the initial string.

    # t = ax.text(
    #     0, 1, "Direction", ha="center", va="center", rotation=0, size=15,
    #     bbox=dict(boxstyle="rarrow", fc="w", ec="black", lw=2))
    t = ax.text(
        46.5, -50, result_infos, ha="center", va="center", rotation=0, size=10,
        bbox=dict(boxstyle="rarrow", fc="w", ec="black", lw=2, alpha=0.6))
    bb = t.get_bbox_patch()
    bb.set_boxstyle("Round", pad=0.6)

    plt.savefig(save_pic_name_path)
    plt.close()

    # plt.show()












