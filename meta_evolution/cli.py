import argparse
import logging
from .config import Config
from .core import MetaEvolutionCore, InputItem


def setup_logging(log_dir):
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=str(log_dir / 'meta_evolution.log'), level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def main():
    parser = argparse.ArgumentParser(prog='meta-evolution')
    parser.add_argument('--config', help='Path to YAML or JSON config file')
    sub = parser.add_subparsers(dest='cmd', required=True)
    run_p = sub.add_parser('run')
    run_p.add_argument('--input', required=True)
    run_p.add_argument('--kind', default='text')
    args = parser.parse_args()
    cfg = Config.from_file(args.config) if args.config else Config.default()
    setup_logging(cfg.log_dir)
    core = MetaEvolutionCore(cfg)
    rep = core.cycle(InputItem(kind=args.kind, payload=args.input, meta={'intent': 'cli'}))
    print(rep.to_dict())

if __name__ == '__main__':
    main()
