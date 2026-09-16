import argparse
from recall.db import connect
from recall.store import save, find


def main() -> None:
    parser = argparse.ArgumentParser(prog="recall")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # save subcommand
    save_p = subparsers.add_parser("save", help="Save a new item")
    save_p.add_argument("--kind", required=True, choices=["link", "snippet", "note"])
    save_p.add_argument("--title", default="")
    save_p.add_argument("--note", default="")
    save_p.add_argument("--content", default="")
    save_p.add_argument("--url", default=None)
    save_p.add_argument("--lang", default=None)

    # find subcommand
    find_p = subparsers.add_parser("find", help="Search saved items")
    find_p.add_argument("query")
    find_p.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()
    conn = connect()

    if args.command == "save":
        new_id = save(
            conn,
            kind=args.kind,
            title=args.title,
            note=args.note,
            content=args.content,
            url=args.url,
            lang=args.lang,
        )
        print(f"saved: {new_id}")

    elif args.command == "find":
        results = find(conn, args.query, limit=args.limit)
        if not results:
            print("no matches")
            return
        for row in results:
            print(f"[{row['id']}] {row['kind']:8} {row['title']}")
            if row['excerpt']:
                print(f"          {row['excerpt']}")