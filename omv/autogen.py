from os.path import isdir, join, split
from glob import glob
import yaml

dirs_to_engines_exts = {'NEURON': {'engine': 'NEURON', 'extension': '.hoc'},
                        'NeuroML2': {'engine': 'LEMS', 'extension': '.nml'}}


def read_option(options, default=0):
    for i, opt in enumerate(options):
        print '\t\t', i, opt
    opt = None
    while opt is None:
        try:
            sel = int(
                raw_input('Select option number [default: %s]: ' % default))
            opt = options[sel]
        except IndexError:
            print 'invalid index!'
        except ValueError:
            print 'selecting default: ', default
            opt = options[default]
    return opt


def find_targets(auto=False):
    targets = []
    for d, eng_ext in dirs_to_engines_exts.iteritems():
        if isdir(d):
            engine = dirs_to_engines_exts[d]['engine']
            ext = dirs_to_engines_exts[d]['extension']
            print 'Default directory for {0} engine found.'.format(engine)
            print '  Will look for scripts with {0} extension'.format(ext)
            scripts = glob(join(d, '*' + ext))
            # print '    found', scripts
            if auto:
                print 'selecting default: ', scripts[0]
                script = scripts[0]
            else:
                script = read_option(scripts)
            targets.append((engine, script))
            # print 'selected', script
    return targets


def create_dryrun(engine, target):
    print ' '.join(('Generating dry run test for file', target,
                    ', using engine', engine))
    dirname, fname = split(target)
    omt = {'target': fname, 'engine': engine}
    with open(target + '.dry.omt', 'w') as fh:
        yaml.dump(omt, fh, default_flow_style=False)


def generate_dottravis(targets):
    env_vars = {'NEURON': "$HOME/neuron/nrn/`arch`/bin",
                'jNeuroML': "$HOME/jnml/jNeuroMLJar"}
    travis = '''\
language: python
python: 2.7

env:
  global:
    - PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python/site-packages PATH={path} {extra_envs}
  matrix:
    - OST_ENGINE=lems
    - OST_ENGINE=neuron

install:
    - pip install git+https://github.com/borismarin/osb-model-validation.git

script:
    - omv_alltests
'''.format(path=':'.join(["$PATH", "$HOME/neuron/nrn/`arch`/bin", "$HOME/jnml/jNeuroMLJar"]),
           extra_envs="JNML_HOME=$HOME/jnml/jNeuroMLJar")

    with open('.travis.yml', 'w') as fh:
        fh.write(travis)


def autogen(auto=False, dry=True):
    targets = find_targets(auto)
    for engine, target in targets:
        if dry:
            create_dryrun(engine, target)
    generate_dottravis(targets)


if __name__ == '__main__':
    autogen()
