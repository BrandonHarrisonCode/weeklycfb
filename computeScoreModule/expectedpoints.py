import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
downs = [dynamodb.Table('1stDowns'),
         dynamodb.Table('2ndDowns'),
         dynamodb.Table('3rdDowns'),
         dynamodb.Table('4thDowns')]


def get_expected_points(down, yards_to_goal, distance):
    table = get_table(down)

    yards_to_goal = str(validate_yards_to_goal(yards_to_goal))
    distance = str(validate_distance(distance))

    response = table.get_item(Key={
        'YardsToGoal': Decimal(yards_to_goal),
    })
    ans = response['Item'][distance]
    return ans


def get_table(down):
    down = validate_down(down)
    return downs[down - 1]


def validate_down(down):
    down = int(down)
    if down < 1:
        down = 1
    elif down > 4:
        down = 4
    return down


def validate_yards_to_goal(yards_to_goal):
    yards_to_goal = int(yards_to_goal)
    if yards_to_goal < 1:
        yards_to_goal = 1
    elif yards_to_goal > 99:
        yards_to_goal = 99
    return yards_to_goal


def validate_distance(distance):
    distance = int(distance)
    if distance < 1:
        distance = 1
    elif distance > 15:
        distance = 15
    return distance
