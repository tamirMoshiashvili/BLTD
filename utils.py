import math


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def dist_score(current_point, danger, target_point):
    return distance(current_point, target_point)


def danger_score(current_point, danger, target_point, dist_weight=0.2, danger_weight=0.8):
    dist = dist_weight * distance(current_point, target_point)
    score1 = dist_weight * distance(current_point, target_point)
    score2 = danger_weight * danger
    return dist + dist * danger * 2
