from textwrap import indent


def print_task_config(config):
    output_str = '\n'.join("%15s: %s" % (key, value) for key, value in config.items())
    print(indent(output_str, '   '))


class CLILogger:

    def __init__(self, task):
        self.task = task

    def __enter__(self):
        print('===========================')
        print(f'Task {self.task.name} started...')
        print('Configuaration:')
        print_task_config(self.task.configuration)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Done!')
