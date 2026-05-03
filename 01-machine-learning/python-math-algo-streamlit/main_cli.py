# main_cli.py
import argparse
from controllers.pipeline_controller import PipelineController

def main():
    ap = argparse.ArgumentParser(description='ARCH E pipeline CLI (MVC)')
    ap.add_argument('--logs', required=True)
    ap.add_argument('--notes', required=True)
    ap.add_argument('--sep', default=',')
    ap.add_argument('--success-threshold', type=float, default=10.0)
    ap.add_argument('--outdir', default='outputs')
    args = ap.parse_args()

    controller = PipelineController(
        logs_path=args.logs,
        notes_path=args.notes,
        sep=args.sep,
        success_threshold=args.success_threshold,
        outdir=args.outdir
    )
    metrics = controller.run()
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()
