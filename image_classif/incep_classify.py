import numpy as np
import tensorflow as tf
from os import listdir, rename
import fnmatch

imagePath = 'images/tweets_attached/'
modelFullPath = 'image_classif/retrained_graph.pb'
labelsFullPath = 'image_classif/retrained_labels.txt'


class ImageClassifier():
    def __init__(self, path_dir=None):
        self.path_dir = path_dir

    def classify_dir(self):
        """Run inference on image over all images on give directory.
        Returns an iterator for performance.
        """
        path_dir = self.path_dir
        files = (path_dir + f for f in listdir(path_dir))
        for image in files:
            try:
                yield (image, self._run_inference_on_image(image))
            except tf.errors.InvalidArgumentError:
                videos = "images/videos/"
                name = image.split('/')[-1]
                rename(image, videos + name)

                print(image)

    def classify_file(self, imagePath):
        """Run inference on only one image.
        To test the classifier."""
        imagePath = self.imagePath
        return self._run_inference_on_image(imagePath)

    def _format_from_label(self, label):
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

    def _create_graph(self):
        """Creates a graph from saved GraphDef file and returns a saver."""
        # Creates graph from saved graph_def.pb.
        with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def _run_inference_on_image(self, imagePath):
        answer = None

        if not tf.gfile.Exists(imagePath):
            tf.logging.fatal('File does not exist %s', imagePath)
            return answer

        image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

        # Creates graph from saved GraphDef.
        self._create_graph()

        with tf.Session() as sess:

            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-5:][::-1]  # Get top 5 predictions
            f = open(labelsFullPath, 'rb')
            lines = f.readlines()
            labels = [str(w).replace("\n", "") for w in lines]
            for node_id in top_k:
                human_string = labels[node_id]
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))

            label = self._format_from_label(labels[top_k[0]])
            answer = label, predictions[top_k[0]]
            return answer


if __name__ == '__main__':
    a = ImageClassifier(imagePath)
    utils = "images/utiles/"
    inutils = "images/inutiles/"
    jpg = len(fnmatch.filter(listdir(imagePath), '*.jpg'))
    png = len(fnmatch.filter(listdir(imagePath), '*.png'))
    advertisement = "\t\t\t++++++++++++++++++\n   \
                     {} JPG's files    \n   \
                     and {} PNG's files\n   \
                     will be classified\n   \
                     ++++++++++++++++++"
    ngb = 2
    while jpg != 0 and png != 0:
        print(advertisement.format(jpg, png))
        try:
            for image, infer in a.classify_dir():
                name = image.split('/')[-1]
                if infer[0] != 'neither':
                    rename(image, utils + name)
                else:
                    rename(image, inutils + name)
                print(image, infer)
        except ValueError:
            warning = "\t\t\t----------------------------\n \
                       ----------------------------\n \
                        WARNING {} GB in your RAM!!\n \
                        YOU CAN STOP AND CONTINUE  \n \
                            LATER IF YOU WISH      \n \
                        ---------------------------\n \
                        ---------------------------"
            print(warning.format(ngb))
            jpg = len(fnmatch.filter(listdir(imagePath), '*.jpg'))
            png = len(fnmatch.filter(listdir(imagePath), '*.png'))
            ngb += 2
            pass
