import sys
import datetime
import click
import json
import tinydb
import pandas
import numpy as np
from pyshlist import backend, gui

class Args(object):
    
    def __init__(self):
        self._database = None
        self.purchases = None
        self.comparisons = None
        
    def open_database(self, file):
        """Opens the tinydb database"""
        self._database = tinydb.TinyDB(file)
        self.purchases = backend.Purchases(self._database)
        self.comparisons = backend.Comparisons(self._database)
        
    def close_database(self):
        self._database.close()


args_config = click.make_pass_decorator(Args, ensure=True)

@click.group()
@click.argument("file", type=click.File('w+'), required=True)
@args_config
def main(args, file):
    file.close()
    args.open_database(file.name)
 
@main.command()
@click.option("--name", type=click.STRING, required=True, help="A unique name for the wishlist item")
@click.option("--price", type=click.FLOAT, required=True, help="The price of the item")
@click.option("--due", type=click.STRING, required=True, help="The due date of the item in YYYY-MM-DD")
@click.option("--category", type=click.STRING, required=False, default=None, help="A category in which the item fits")
@click.option("--description", type=click.STRING, required=False, default=None, help="The description of the item")
@args_config
def add(args, name, price, due, category=None, description=None):
    """Adds an item to the wishlist"""
    args.purchases.new(name, price, due, 0, category, description)


@main.command()
@args_config
def addg(args):
    """Opens a GUI to add a new purchase to the list"""
    data = gui.purchase()
    if data:
        args.purchases.new(**data)
        
@main.command()
@args_config
def rate(args):
    """Rate items regarding desirability (GUI only)"""
    for comparison in args.comparisons.missing_comparisons:
        result = gui.compare(comparison[0], comparison[1])
        if result['canceled']:
            args.close_database()
            sys.exit()
        else:
            args.comparisons.vote(comparison[0], comparison[1], result['a_more_important'])

@main.command()
@args_config
def dump(args):
    """Prints the wishlist"""
    print(pandas.DataFrame.from_dict(args.comparisons.rated_purchases))
    
@main.command()
@click.option("--name", type=click.STRING, required=True, help="Name of the item to remove")
@args_config
def remove(args, name):
    """Removes an item from the wishlist"""
    item_found = args.purchases.remove(name)
    if item_found:
        args.comparisons.prune()
    else:
        print('Item "%s" not found' % name, file=sys.stderr)
    


@main.command()
@click.option("--output", type=click.STRING, required=False, default=None, help="Filename as which to save the plot")
@args_config
def plot(args, output = None):
    """Creates the purchase scatter plot"""
    import matplotlib.pyplot as plt
    
    def random_position():
        return np.random.randn() * 10 + 20
    
    today = datetime.datetime.now()
    data = pandas.DataFrame.from_dict(args.comparisons.rated_purchases)
    data['due_date'] = data['due_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    data['time_left'] = data['due_date'].apply(lambda x: (x - today).days)
    data['price'] = data['price'].apply(lambda x: float(x))
    
    categories = args.purchases.categories
    categories = { c : 0.1 + float(idx) / len(categories) for idx, c in enumerate(categories) }
    colors = data['category'].apply(lambda x: categories[x])
    
    xdata = np.array(data['time_left'])
    xdata -= np.min(xdata)
    xdata = xdata / np.max(xdata)
    #xdata = 1.0 - xdata
    xlabels = np.array(data['time_left'])
    ydata = data['desirability'].fillna(0)
    ylabels = np.array(ydata)
    labels = data['name']
    size = data['price']
    
    fig = plt.figure(1)
    ax = fig.gca()
    plt.scatter(x=xdata, y=ydata, s=size, c=colors, cmap = plt.get_cmap('gist_rainbow'))
    plt.grid()
    plt.axis([-0.2, 1.2, -0.2, 1.2])
    plt.axes().set_aspect('equal')
    plt.xlabel("Days left")
    plt.ylabel("Desirability")
    plt.xticks(xdata, xlabels)
    plt.yticks(ydata, ylabels)
    ax.yaxis.set_ticklabels([])
    for label, x, y in zip(labels, xdata, ydata):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (random_position(), random_position()),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
            
    if output is None:
        plt.show()
    else:
        plt.savefig(output)
