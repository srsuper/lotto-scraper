import argparse
import csv

import lotto_scraper as lotto


csv_fname = 'lotto.csv'

def all_main():
    print('-----> All Mode')
    all_list = lotto.get_all_numbers()

    with open(csv_fname, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_list)

def one_main(draw_no):
    print('-----> One Mode: {}'.format(draw_no))
    new_tuple = lotto.get_numbers(draw_no)

    # csv파일의 마지막 라인에 저장된 last 회차(draw_no)를 read
    with open(csv_fname) as f:
        reader = csv.reader(f)
        for row in reader:
            pass
        last_row = list(map(int, row))

    # 회차(draw_no) 정보를 비교
    if new_tuple[0] == last_row[0] + 1:
        with open(csv_fname, 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(new_tuple)
        print('Updated new draw_no({}).'.format(new_tuple[0]))
    # 이미 last에 저장된 정보와 동일한 회차를 땡겨온 경우
    elif new_tuple[0] == last_row[0]:
        print('Already updated the draw_no({}).'.format(new_tuple[0]))
    else:
        raise Exception('Invalid draw_no(new, last)', new_tuple[0], last_row[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--num', type=int, default=0)
    args = parser.parse_args()

    print(args)

    if args.all:
        # all numbers
        all_main()
    else:
        # one numbers : if args.num is 0, last draw_no
        one_main(args.num)
