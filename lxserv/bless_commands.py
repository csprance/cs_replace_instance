import lx
import modo

import cs_replace_instance

class ReplaceInstanceCommandClass(cs_replace_instance.CommanderClass):


    def commander_execute(self, msg, flags):
        reload(cs_replace_instance)
        cs_replace_instance.main()


lx.bless(ReplaceInstanceCommandClass, "cs_replace_instance.replace")
