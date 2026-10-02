import argparse
import sys

from toolkit import calculator, converter, errors


# создаем парсер для команды
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="toolkit")
    subparsers = parser.add_subparsers(dest="command")

    calc_parser = subparsers.add_parser("calc")
    calc_parser.add_argument("expression")

    convert_parser = subparsers.add_parser("convert")
    convert_parser.add_argument("value", type=float)
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # если вызван калькулятор, вызываем калькулятор
    if args.command == "calc":
        try:
            print(calculator.calculation(calculator.tokenize(args.expression)),file=sys.stdout)
            sys.exit(0)
        except errors.ToolkitError as e:
            print(e,file=sys.stderr)
            sys.exit(2)

    # если конвертер - конвертер
    elif args.command == "convert":
        try:
            print(converter.convert(args.value, args.from_unit, args.to_unit), file=sys.stdout)
            sys.exit(0)
        except errors.ToolkitError as e:
            print(e, file=sys.stderr)
            sys.exit(2)

    # иначе это неизвестная команда
    else:
        print("Ошибка! Неизвестная команда", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()