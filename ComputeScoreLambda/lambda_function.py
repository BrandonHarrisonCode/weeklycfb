from winprobability import play_win_probability

def lambda_handler(event, context):
    ans = play_win_probability()

    return {
        'statusCode': 200,
        'body': ans
    }


if __name__ == '__main__':
    print(lambda_handler(None, None))
