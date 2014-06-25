import os
import subprocess as sp

from ..common.output import inform
from backend import OMVBackend

class JNeuroMLBackend(OMVBackend):

    name = "jNeuroML"
        
    @staticmethod
    def is_installed(version):
        print("Checking whether %s is installed..."%JNeuroMLBackend.name)
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['jnml', '-h'], stdout=FNULL)
        except OSError:
            ret = False
        return ret
        
    def install(self, version):
        from getjnml import install_jnml
        home = os.environ['HOME']
        p = os.path.join(home, 'jnml/jNeuroMLJar')
        self.path = p
        self.environment_vars = {'JNML_HOME': p}
        inform('Will fetch and install the latest jNeuroML jar', indent=2)
        install_jnml()

    def run(self):
        try:
            self.stdout = sp.check_output(['jnml', self.modelpath, '-nogui'])
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output


















