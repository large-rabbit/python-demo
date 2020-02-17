"""
井字棋

Version: 1.0
Author: large-rabbit
"""
import os


def print_board(map_arr):
    """
    画出棋盘

    :param map_arr: 棋盘的地图数组
    :return: None
    """
    os.system('cls')
    for col in range(3):
        print(map_arr[col * 3 + 0] + '|' + map_arr[col * 3 + 1] + '|' + map_arr[col * 3 + 2])
        if col != 2:
            print('-+-+-')


def decide_win(map_arr):
    """
    判断输赢

    :param map_arr: 棋盘的地图数组
    :return: 胜利方:'X'、'O'、'平局'
    """
    who_win = decide_row(map_arr)
    if who_win == '平局':
        who_win = decide_col(map_arr)
        if who_win == '平局':
            who_win = decide_across(map_arr)
    return who_win


def decide_row(map_arr):
    """
    判断横向是否有胜负

    :param map_arr: 棋盘的地图数组
    :return: 胜利方:'X'、'O'、'平局'
    """
    for col in range(3):
        tem_arr = map_arr[col*3:col*3+3]
        result = detect_win(tem_arr)
        if result != '平局':
            return result
    return '平局'


def decide_col(map_arr):
    """
    判断纵向是否有胜负

    :param map_arr: 棋盘的地图数组
    :return: 胜利方:'X'、'O'、'平局'
    """

    for row in range(3):
        tem_arr = [map_arr[col * 3 + row] for col in range(3)]
        result = detect_win(tem_arr)
        if result != '平局':
            return result
    return '平局'


def decide_across(map_arr):
    """
    判断对角是否有胜负

    :param map_arr: 棋盘的地图数组
    :return: 胜利方:'X'、'O'、'平局'
    """
    tem_arr = [map_arr[0], map_arr[4], map_arr[8]]
    result = detect_win(tem_arr)
    if result != '平局':
        return result
    tem_arr = [map_arr[2], map_arr[4], map_arr[6]]
    result = detect_win(tem_arr)
    if result != '平局':
        return result
    return '平局'


def detect_win(tem_arr):
    if tem_arr == ['X', 'X', 'X']:
        return 'X胜'
    elif tem_arr == ['O', 'O', 'O']:
        return 'O胜'
    else:
        return '平局'


def main():
    is_again = True
    while is_again:
        map_arr = [' '] * 9
        is_continue = True
        who_win = 0
        turn = 'X'
        count = 0
        print_board(map_arr)
        while is_continue:
            is_input = True
            while is_input:
                print('{0}出棋'.format(turn))
                try:
                    x = int(input('请输入X坐标(从0开始，2结束)：'))
                    y = int(input('请输入y坐标(从0开始，2结束)：'))
                    if 0 <= x <= 2 and 0 <= y <= 2 and map_arr[3 * y + x] == ' ':
                        map_arr[3 * y + x] = turn
                        turn = 'O' if turn == 'X' else 'X'
                        is_input = False
                    else:
                        print('坐标有误，请重新输入')
                except ValueError:
                    print('坐标有误，请重新输入')
            print_board(map_arr)
            who_win = decide_win(map_arr)
            if who_win == '平局':
                if count == 8:
                    is_continue = False
                else:
                    is_continue = True
            else:
                is_continue = False
            count += 1
        os.system('cls')
        print('=' * 12)
        print('该局为：{0}'.format(who_win))
        print('=' * 12)
        choice = input('是否再来一局？yes|no：')
        is_again = choice == 'yes'


if __name__ == '__main__':
    main()
