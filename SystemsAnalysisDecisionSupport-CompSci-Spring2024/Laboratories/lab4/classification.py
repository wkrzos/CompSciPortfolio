from typing import List, Tuple

def get_confusion_matrix(
    y_true: List[int], y_pred: List[int], num_classes: int,
) -> List[List[int]]:
    """
    Generate a confusion matrix in a form of a list of lists. 

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values
    :param num_classes: number of supported classes

    :return: confusion matrix
    """
    
    """
    FAILED test_classification.py::test_cm_incorrect_prediction_classes[y_true0-y_pred0-3] - IndexError: list index out of range
    FAILED test_classification.py::test_cm_incorrect_prediction_classes[y_true1-y_pred1-3] - IndexError: list index out of range 
    """
    
    if len(y_true) != len(y_pred):
        raise ValueError("Invalid input shapes!")
    
    matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
    
    for true, pred in zip(y_true, y_pred):
        if pred >= num_classes:
            raise ValueError("Invalid prediction classes!")
        matrix[true][pred] += 1
        
    return matrix


def get_quality_factors(
    y_true: List[int],
    y_pred: List[int],
) -> Tuple[int, int, int, int]:
    """
    Calculate True Negative, False Positive, False Negative and True Positive 
    metrics basing on the ground truth and predicted lists.

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: a tuple of TN, FP, FN, TP
    """
    TN, FP, FN, TP = 0, 0, 0, 0
    
    for true, pred in zip(y_true, y_pred):
        if true == pred == 0:
            TN += 1
        elif true == 0 and pred == 1:
            FP += 1
        elif true == 1 and pred == 0:
            FN += 1
        elif true == pred == 1:
            TP += 1
            
    return TN, FP, FN, TP

def accuracy_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the accuracy for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: accuracy score
    """
    correct_predictions = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct_predictions / len(y_true)


def precision_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the precision for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: precision score
    """
    TN, FP, FN, TP = get_quality_factors(y_true, y_pred)
    return TP / (TP + FP) if (TP + FP) else 0


def recall_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the recall for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: recall score
    """
    TN, FP, FN, TP = get_quality_factors(y_true, y_pred)
    return TP / (TP + FN) if (TP + FN) else 0


def f1_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the F1-score for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: F1-score
    """
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0