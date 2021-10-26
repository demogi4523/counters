import click
from tabulate import tabulate

from storage import Storage

db = Storage()

@click.group()
def cli():
    pass


@click.command()
@click.argument('name')
@click.argument('_type', required=False)
@click.argument('desc', required=False)
def create(name, _type=0, desc=None):
    """Create new counter"""
    click.echo(f'Create {name} of my_type: {_type} \n\n {desc}')
    db.create_counter(name, desc, _type)


@click.command()
@click.argument('counter_name')
@click.argument('value')
@click.argument('comment', required=False)
def add(counter_name, value, comment=''):
    """Update counter"""
    click.echo(f'Update {counter_name} with value: {value} \n\n {comment}')
    db.update_counter(counter_name, value, comment)


@click.command()
@click.argument('counter_name')
def delete(counter_name):
    """Delete counter"""
    click.echo(f'Delete {counter_name}')
    db.remove_counter(counter_name)


# @click.command()
# def show(name):
#     """Show counter"""
#     click.echo(f'{name}')


# @click.command()
# def use(counter, my_type=0, desc=None):
#     """Using counter for further manipulation"""
#     click.echo(f'Using {counter}')


@click.command()
# @click.option('--from', help='filter by starting date')
# @click.option('--to', help='filter by ending date')
# @click.option('--sort', default=False, help='sort by increase')
def ls():
    """Show list of counters"""
    counters = db.get_counters()
    # click.echo(f'{counters}')
    print(tabulate(counters, headers=['Counter', 'Sum'], tablefmt='orgtbl'))
    


# @click.command()
# def remind(name, date_and_time, msg):
#     """Remind about counter"""
#     click.echo(f'You will be reminded about {name} at {date_and_time}')


# @click.command()
# def restore():
#     """Restore your data"""
#     click.echo(f'We restore all your data')


# @click.command()
# def backup():
#     """Backup your data"""
#     click.echo(f'All your data was backuped')


commands = [
    add,
    create,
    delete,
    # show,
    # use,
    ls,
    # remind,
    # restore,
    # backup,
]

for command in commands:
    cli.add_command(command)

if __name__ == '__main__':
    cli()
