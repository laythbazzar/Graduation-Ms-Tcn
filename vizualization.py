import matplotlib.pyplot as plt
import colorcet as cc
import argparse
import os
import matplotlib
matplotlib.use('Agg')

# from matplotlib.patches import ConnectionPatch

# FrameVideo1 = 100
# FrameVideo2=600

# files for mapping and samples
def read_file(path):
    with open(path, 'r') as f:
        content = f.read()
        f.close()
    return content

def main():
    # plt.use('inline')
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', default="gtea")
    parser.add_argument('--split', default='1')

    args = parser.parse_args()

    ground_truth_path = "/content/drive/MyDrive/data/" + args.dataset + "/groundTruth/"
    recog_path = "/content/drive/MyDrive/results/" + args.dataset + "/split_" + args.split + "/"
    file_list = "/content/drive/MyDrive/data/" + args.dataset + "/splits/test.split" + args.split + ".bundle"
    mapping_file = "/content/drive/MyDrive/data/" + args.dataset + "/mapping.txt"
    visual_file = "/content/drive/MyDrive/visualization/" + args.dataset + "/split_" + args.split + "/"

    directory = '/content/drive/MyDrive/visualization/gtea/split_' + args.split
    print (directory)
    if not os.path.exists(directory):
      os.makedirs(directory)

    list_of_videos = read_file(file_list).split('\n')[:-1]

    # MapLabelNumber and MapNumberLabel maps numbers to labels and vice versa
    MapLabelNumber = {}
    MapNumberLabel = {}
    colors = []
    with open(mapping_file, 'r') as mfp:
        for line in mfp:
            values = line.strip().split()
            if len(values) == 2:
                num, label = values
                try:
                    num = int(num)
                except ValueError:
                    print(f"Invalid number '{num}' on line '{line}' from map file")
                    continue
                MapLabelNumber[label] = num
                MapNumberLabel[num] = label

    # colors depending on the number of labels
    colors = cc.glasbey_light[:len(MapNumberLabel)]

    for vid in list_of_videos:
        gt_file = ground_truth_path + vid
        gt_content = []

        recog_file = recog_path + vid.split('.')[0]
        recog_content = []

        with open(recog_file, 'r') as lfp:
            for line in lfp:
                if line.startswith("#"):
                    continue
                for word in line.split():
                    # values = line.strip()
                    recog_content.append(MapLabelNumber[word])
            # read_file(gt_file).split('\n')[0:-1]

        with open(gt_file, 'r') as lfp:
            for line in lfp:
                if line.startswith("#"):
                    continue
                for word in line.split():
                    # values = line.strip()
                    gt_content.append(MapLabelNumber[word])

        MaxFrames = max(len(gt_content), len(recog_content))  # decide the limit for x-axis depending on the length of the two videos
        # plot two subplots
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 2))
        fig.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)
        # ax1.set_aspect()

        # plotting the first subplot
        x_pos = 0
        for label in recog_content:
            ax1.barh(0, 1, left=x_pos, height=1, color=colors[label])
            x_pos += 1
        ax1.set_xlim([0, len(gt_content)])
        ax1.set_yticks([])
        ax1.set_xticks([])

        # plotting the second subplot
        x_pos = 0
        for label in gt_content:
            ax2.barh(0, 1, left=x_pos, height=1, color=colors[label])
            x_pos += 1
        ax2.set_xlim([0, len(gt_content)])
        ax2.set_yticks([])
        ax2.set_xticks([])

        # add text
        x_pos = 0.02
        for i in MapNumberLabel:
            ax2.text(x_pos, -0.18, MapNumberLabel[i], ha='center', color=colors[i], transform=ax2.transAxes)
            x_pos += (len(MapNumberLabel[i]) + 1) / 70

        # delete the boarders
        ax1.spines["top"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["left"].set_visible(False)
        ax1.spines["right"].set_visible(False)

        ax2.spines["top"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["right"].set_visible(False)

    # xyA = (FrameVideo1/MaxFrames, -0.5)  # Center of the first subplot
    # xyB = (FrameVideo2/MaxFrames, 0.5)    # Left edge of the second subplot
    #
    # Create the ConnectionPatch object with the arrow properties
    # con = ConnectionPatch(
    #     xyA=xyA, coordsA=ax1.get_yaxis_transform(),
    #     xyB=xyB, coordsB=ax2.get_yaxis_transform(),
    #     arrowstyle="<|-|>,head_width=0.2", color='black')
    #
    # # Add the arrow to the second subplot
    # ax2.add_artist(con)

        ax1.annotate('Prediction:', xy=(-0.01, 0.5), xycoords='axes fraction',
                     fontsize=12, ha='right', va='center', weight='bold')

        ax2.annotate('Truth:', xy=(-0.01, 0.5), xycoords='axes fraction',
                     fontsize=12, ha='right', va='center', weight='bold')

        plt.savefig( visual_file + vid.split('.txt')[0] + ".png")
        print (vid.split('.txt')[0])
if __name__ == '__main__':
    main()