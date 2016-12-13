import sys
import cv2
import time
import Queue
import numpy
import builddata
import emotionclassifier


def main():
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        if mode == 'train':
            if len(sys.argv) > 5:
                start = time.clock()
                faces = builddata.get_data(sys.argv[2], int(sys.argv[5]))
                training_data, testing_data = emotionclassifier.divide_data(faces, 0.1)
                print 'number of training examples = ' + str(len(training_data))
                print 'number of testing examples  = ' + str(len(testing_data)) + '\n'

                classifier = emotionclassifier.EmotionClassifier(int(sys.argv[5]), sys.argv[3])
                accuracy = classifier.train(training_data, testing_data, epochs=int(sys.argv[4]), intervals=1)
                end = time.clock()
                print 'Testing Accuracy: ' + '{:.9f}'.format(accuracy)
                print 'Training Time: ' + '{:.2f}'.format(end - start) + 's'
            else:
                print 'Please add \'Image Dir\' \'Session Save Path\' \'Number of Epochs\' \'Number of Classes\''

        elif mode == 'classify':
            if len(sys.argv) > 4:
                start = time.clock()
                face = builddata.get_face(sys.argv[2])
                classifier = emotionclassifier.EmotionClassifier(int(sys.argv[4]), sys.argv[3])
                classification = classifier.classify(face)
                end = time.clock()
                print sys.argv[2]+' classified as '+str(numpy.argmax(classification[0])+1)+' in '+str(end-start)+'s'
                print classification[0]
            else:
                print 'Please add \'Image Path\' \'Session Save Path\' \'Number of Classes\''

        elif mode == 'run':
            if len(sys.argv) > 3:
                start = time.clock()
                video = cv2.VideoCapture()
                q = Queue.Queue(10)
                while True:
                    _, frame = video.read()
                    classifier = emotionclassifier.EmotionClassifier(sys.argv[2], sys.argv[1])
                    classification = classifier.classify(frame)
                    q.put(classification)
                    print classification
            else:
                print 'Please add \'Session Save Path\' \'Number of Classes\''

        elif mode == 'build':
            if len(sys.argv) > 4:
                start = time.clock()
                count = builddata.build_data(sys.argv[2], sys.argv[3], sys.argv[4])
                end = time.clock()
                print 'Augmented Dataset built ' + str(count) + ' images in ' + str(end - start) + 's'
            else:
                print 'Please add \'Image Dir\' \'Label Dir\' \'Output Dir\''

        elif mode == 'normalize':
            if len(sys.argv) > 2:
                start = time.clock()
                count = builddata.normalize(sys.argv[2])
                end = time.clock()
                print 'Normalized Dataset ' + str(count) + ' images in ' + str(end - start) + 's'
            else:
                print 'Please add \'Image Dir\''
        else:
            print 'Please add either \'train\', \'classify\' or \'build\' as command line arguments.'

    else:
        print 'Please add either \'train\', \'classify\' or \'build\' as command line arguments.'


if __name__ == '__main__':
    main()
