import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
from sklearn import linear_model, svm, tree
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from draco.learn import data_util
from pprint import pprint


def prepare_data(data: pd.DataFrame):
    """ transform data into X, y matrices
        Returns:
            X: ndarray of shape (2 * N, num_columns), representing matrix
            y: ndarray of shape (2 * N), representing labels
    """
    N = len(data)

    X = np.zeros((2 * N, len(data.positive.columns)))
    y = np.zeros(2 * N)

    for i in range(N):
        x_pos = data.positive.iloc[i].values
        x_neg = data.negative.iloc[i].values

        X[i] = x_pos - x_neg
        y[i] = 0

        X[i + N] = x_neg - x_pos
        y[i + N] = 1

    return X, y
  

def train_model(X: np.array, y: np.array, split=0.7):
    """ Given features X and labels y, train a linear model to classify them
        Args:
            X: a N x M matrix, representing feature vectors
            y: a N vector, representing labels
            split: the split between train and dev
    """
    X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=split, random_state=1)
    clf = svm.LinearSVC(C=1)
    clf.fit(X_train, y_train)
    print("Train score: ", clf.score(X_train, y_train))
    print("Dev score: ", clf.score(X_dev, y_dev))
    return clf


def train_and_plot(X: np.array, y: np.array, split=0.7):
    """ Reduce X, y into 2D using PCA and use SVM to classify them
        Then plot the decision boundary as well as raw data points
    """
    pca = PCA(n_components=2)
    X = pca.fit_transform(X)

    clf = train_model(X, y, split)

    # for plotting
    X0, X1 = X[:, 0], X[:, 1]
    xx, yy = make_meshgrid(X0, X1)

    cm_bright = ListedColormap(['#FF0000', '#0000FF'])

    f, ax = plt.subplots()
    plot_contours(ax, clf, xx, yy, cmap=cm_bright, alpha=0.2)

    # classes labeled 0
    idx = (y == 0)
    plt.scatter(X0[idx], X1[idx], c='r', cmap=cm_bright, alpha=0.5, marker='>', label='positive')
    plt.scatter(X0[~idx], X1[~idx], c='b', cmap=cm_bright, alpha=0.5, marker='<', label='negative')

    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())

    ax.set_xlabel('X0')
    ax.set_ylabel('X1')

    ax.set_xticks(())
    ax.set_yticks(())

    plt.legend(loc='lower right')
    plt.axis("tight")

    plt.show()

    return clf


def train_and_plot2(X: np.array, y: np.array, split=0.7):
    """ Reduce X, y into 2D using PCA and use SVM to classify them
        Then plot the decision boundary as well as raw data points
    """
    pca = PCA(n_components=2)
    X2 = pca.fit_transform(X)

    clf = train_model(X, y, split)

    # for plotting
    X0, X1 = X2[:, 0], X2[:, 1]
    xx, yy = make_meshgrid(X0, X1)

    cm_bright = ListedColormap(['#FF0000', '#0000FF'])

    f, ax = plt.subplots()

    # predictions made by the linear model
    pred = clf.predict(X)

    l = np.copy(y)
    for i in range(len(pred)):
        l[i] = pred[i] * 2 + y[i]

    #label: 00 -> correct
    #       11 -> correct
    #       10 -> wrong, predict 0 to 1
    #       01 -> wrong, predict 0 to 1

    # classes labeled 0
    plt.scatter(X0[l==0], X1[l==0], c='b', cmap=cm_bright, alpha=0.5, marker='>', label='positive')
    plt.scatter(X0[l==2], X1[l==2], c='y', cmap=cm_bright, alpha=0.5, marker='>', label='positive')
    plt.scatter(X0[l==3], X1[l==3], c='r', cmap=cm_bright, alpha=0.5, marker='<', label='negative')
    plt.scatter(X0[l==1], X1[l==1], c='g', cmap=cm_bright, alpha=0.5, marker='>', label='positive')

    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())

    ax.set_xlabel('X0')
    ax.set_ylabel('X1')

    ax.set_xticks(())
    ax.set_yticks(())

    plt.legend(loc='lower right')
    plt.axis("tight")

    plt.show()

    return clf


def plot_contours(ax, clf, xx, yy, **params):
    """Plot the decision boundaries for a classifier.
    Params:
        ax: matplotlib axes object
        clf: a classifier
        xx: meshgrid ndarray
        yy: meshgrid ndarray
        params: dictionary of params to pass to contourf, optional
    """
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out

def make_meshgrid(x, y, h=.02):
    """Create a mesh of points to plot in
    Params:
        x: data to base x-axis meshgrid on
        y: data to base y-axis meshgrid on
        h: stepsize for meshgrid, optional
    Returns:
        xx, yy : ndarray
    """
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy


def main():
    train_dev, _  = data_util.load_data()
    X, y = prepare_data(train_dev)
    return train_and_plot2(X, y)
    
if __name__ == '__main__':
    main()
