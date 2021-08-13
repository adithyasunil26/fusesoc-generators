#!/usr/bin/env python
from fusesoc.capi2.generator import Generator
import subprocess
import json

class BSGFakeramGenerator(Generator):
    def run(self):
        path_to_cfg = self.config.get('path_to_cfg', 'example_cfgs/freepdk45.cfg')

        rd = '../../bsg_fakeram_0-r1'

        sd = subprocess.Popen( 'pwd', stdout=subprocess.PIPE).communicate()[0]
        sd = str(sd).split("'")[1]
        sd = sd.split("\\n")[0]
        
        args = ['cp', '-rf','../bsg_fakeram_gen_0-r1/Makefile','Makefile']
        rc = subprocess.call(args, cwd=rd)

        args = ['make', 'tools']
        rc = subprocess.call(args, cwd=rd)

        args = ['cp', path_to_cfg,'./conf.cfg']
        rc = subprocess.call(args, cwd=rd)

        args = ['make', 'run']
        rc = subprocess.call(args, cwd=rd)

        f = open(path_to_cfg)
        data=json.load(f)
        for i in data["srams"]:
            a = i["name"]
            to = sd+'/{}.v'.format(a)
            args = ['cp', '-rf','results/{}/{}.v'.format(a,a),to]
            rc = subprocess.call(args, cwd=rd)
            self.add_files([{ '{}.v'.format(a) : {'file_type' : 'verilogSource'}}])
        
        if rc:
            exit(1)

g = BSGFakeramGenerator()
g.run()
g.write()
