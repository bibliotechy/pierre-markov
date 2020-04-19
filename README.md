# Pierre Markov, Author of the Quixote

Some python scripts to recreate the central absurdity of [Pierre Menard, Author of the Quixote](https://en.wikipedia.org/wiki/Pierre_Menard,_Author_of_the_Quixote) using variations on a markov chain. It biols down to a ptyhon command that will generate a fragment of Don Quixote from the text of Quixote itself. 


## Setup

### Dependencies
You'll need to have pipenv installed for some dependencies.

This work also currently depends on levelDB, whcih you may or may not have to install. The [plyvel](https://plyvel.readthedocs.io/en/latest/installation.html#installation-guide) can help out there.

Run `pipenv install --dev` to install dependenices

and then `pipenv shell` to open a shell where all the dependencies are available.

### Build the source database

Now we build the source database. Run:

`python populate_db.py`

and about a minute later the database will be created. BY default, it soties the requires files in the local directory `./dqdb`.

By default, the only data added to the directory is taken form the text of Don Quixote, stored in the root of this repository `don-quixote.txt`. You can add other text to the database by using the `-f` flag and passing another file. 

## Making fragments of Quixote

Now you can make fragments of Quixote by running

`python make.py`

which should return somethign like

```
un grosero villano, o un mentecato gracioso, pensarán que yo soy algún echacuervos, o algún caballero de mohatra? No, no, Sancho amigo, huye, huye destos inconvinientes, que quien tropieza en hablador y en gracioso, al primer puntapié cae y da en truhán desgraciado. Enfrena la lengua, considera y rumia las palabras antes que te salgan de la boca
```
