import numpy as np
import tensorflow as tf

imagePath = 'rio.jpg'
modelFullPath = 'retrained_graph.pb'
labelsFullPath = 'retrained_labels.txt'


def format_from_label(label):
    """Just format from label tensorflow classifier output.
    The input format is (correspondly to the tensorflow output):
        "b'LABEL\\n'"
    The output format is:
        'LABEL'
    """
    label = label.split('\'')
    label = label[1].split('\\')
    label = label[0]
    return label


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        label = format_from_label(labels[top_k[0]])
        answer = label, predictions[top_k[0]]
        return answer


if __name__ == '__main__':
    a = run_inference_on_image(imagePath)
    print(a)
