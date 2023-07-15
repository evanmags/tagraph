from tagraph.repo import TagRepo

from pprint import pp

with open("./tags.yml") as f:
    repo = TagRepo(f)

pp(repo.query('*'))
pp(repo.query('*::!pop|funny'))
# pp(repo.query('**'))
# pp(repo.query('**::neuro'))
# pp(repo.query('funny'))
# pp(repo.query('funny::fail'))
# pp(repo.query('funny::*::injury'))
# pp(repo.query('funny::**'))
# pp(repo.query('funny::*::**'))
# pp(repo.query('funny::**::*'))
# pp(repo.query('funny::{!joke}'))
# pp(repo.query('funny::{fail|joke}'))
# pp(repo.query('funny::{fail|!joke}'))
# pp(repo.query('funny::{!fail&!joke}'))
