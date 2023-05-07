from gather_dataset import gather_dataset
from trades_simulation import gather_trades_dataset
from check_trades import gather_trades_analyses
from dump_to_excel import dump_to_excel


def main():
    gather_dataset()
    gather_trades_dataset()
    gather_trades_analyses()
    dump_to_excel()


if __name__ == '__main__':
    main()
