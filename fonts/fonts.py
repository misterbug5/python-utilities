from http import client
import sys, os
from typing import List

class CommandHandler():
    def __init__(self, args: List[str]) -> None:
        if os.geteuid()!=0:
            pass
            # raise PermissionError("You need root access to install fonts")
        self.args = args
        self.dict_args = {'':''}

    def show_help(self)->None:
        print('Usage: sudo python fonts.py [Command] [Font Name] [Options]')
        print('Commands:')
        print('-h     - Shows help')
        print('-i     - Install font')
        print('-u     - Uninstall font')


    def execute(self)->None:
        if len(self.args)==0:
            self.show_help()
            exit(0)
        self.process_args()
        if '-h' in self.dict_args:
            self.show_help()
            return
        if '-i' in self.dict_args:
            self.install()
            return
        if '-u' in self.dict_args:
            self.uninstall()
            return

    def install(self)->None:
        # TODO: Make install process
        myclient = client.HTTPSConnection('github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/'+str.join('', self.dict_args['-i'].title().split(' ')))
        print('https://'+myclient.host)
        print('Installing...', self.dict_args['-i'])

    def uninstall(self)->None:
        # TODO: Make Uninstall process
        print('Uninstalling...', self.dict_args['-u'])
    
    def process_args(self)->None:
        indexes = []

        for arg in self.args:
            if arg.startswith('-'):
                indexes.append(self.args.index(arg))

        if len(indexes) < 1:
            raise SyntaxError('No argument Found use -h for help')

        self.dict_args[self.args[indexes[-1]]]=str.join(' ', self.args[indexes[-1]+1:])

        while len(indexes) > 1:
            self.dict_args[self.args[indexes[-1]]]=str.join(' ', self.args[indexes[-2]+1:indexes.pop()])

if __name__=='__main__':
    del sys.argv[0]
    console = CommandHandler(sys.argv)
    console.execute()
