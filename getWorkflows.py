#!/usr/bin/python
# encoding: utf-8

from __future__ import unicode_literals

import os
import sys
import itertools
from workflow import Workflow3

wf = None
log = None

nothing_found_error_text = 'Nothing found'


def main(wf):

    from plistlib import readPlist
    import glob

    if len(wf.args):
        query = wf.args[0]
    else:
        query = "my workflows"

    p = "/Users/kevinfunderburg/Dropbox/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows"

    log.info(wf.datadir)
    log.info('Workflow response complete')

    ds = os.listdir(p)

    for folder in ds:
        path = p + "/" + folder
        os.chdir(path)

        for file in glob.glob("*info.plist"):
            plPath = path + "/" + file

            if query == "my workflows":
                pl = readPlist(plPath)

                try:
                    if pl["createdby"] == "Kevin Funderburg" and pl["disabled"] == False:

                        _uid = pl["bundleid"]
                        objects = pl["objects"]
                        hotString = ""
                        modString = ""
                        if _uid == "":
                            _uid == pl["name"]
                        _title = pl["name"]

                        for obj in objects:
                            if obj["type"] == "alfred.workflow.trigger.hotkey":
                                modVal = obj["config"]["hotmod"]
                                hotString = obj["config"]["hotstring"]
                                modString += getHotKeys(modVal)
                                if modString != "":
                                    modString += hotString + " "

                        if modString != "":
                            _title = _title + "\t\t\t\t\t\t" + modString

                        it = wf.add_item(title=_title,
                                    subtitle=pl["description"],
                                    arg=path,
                                    autocomplete=pl["name"],
                                    valid=True,
                                    icon=path + "/icon.png",
                                    icontype="file",
                                    quicklookurl=path)

                        it.add_modifier('cmd', subtitle="open workflow folder Finder", arg=path, valid=True)
                        it.add_modifier('alt', subtitle="select in Alfred Preferences", arg=pl["name"], valid=True)

                except Exception:
                    pass
            else:
                try:
                    pl = readPlist(plPath)

                    if not pl["disabled"]:

                        # name = pl["name"]
                        objects = pl["objects"]
                        _uid = pl["bundleid"]
                        hotString = ""
                        modString = ""
                        if _uid == "":
                            _uid == pl["name"]
                        _title = pl["name"]

                        try:
                            for obj in objects:
                                if obj["type"] == "alfred.workflow.trigger.hotkey":
                                    modVal = obj["config"]["hotmod"]
                                    hotString = obj["config"]["hotstring"]
                                    modString += getHotKeys(modVal)
                                    if modString != "":
                                        modString += hotString + " "

                            if modString != "":
                                _title = _title + "\t\t\t\t\t\t" + modString
                        except Exception:
                            pass

                        it = wf.add_item(title=_title,
                                    subtitle=pl["description"],
                                    arg=path,
                                    autocomplete=pl["name"],
                                    valid=True,
                                    icon=path + "/icon.png",
                                    icontype="file",
                                    quicklookurl=path)

                        it.add_modifier('cmd', subtitle="open workflow folder Finder", arg=path, valid=True)
                        it.add_modifier('alt', subtitle="select in Alfred Preferences", arg=pl["name"], valid=True)

                except Exception:
                    pass

    return wf.send_feedback()


def getHotKeys(modVal):
    cmd = 1048576
    opt = 524288
    ctrl = 262144
    shft = 131072
    fn = 8388608

    hotKeyCombos = list()
    modString = ""
    a = [cmd, opt, ctrl, shft, fn]

    for i in range(6):
        hotKeyCombos += list(itertools.combinations(a, i))

    for h in hotKeyCombos:
        theSum = 0
        for n in range(len(h)):
            theSum += h[n]
        if theSum == modVal:
            for n in range(len(h)):
                if h[n] == 0:
                    mod = ""
                elif h[n] == cmd:
                    mod = "⌘"
                elif h[n] == opt:
                    mod = "⌥"
                elif h[n] == ctrl:
                    mod = "⌃"
                elif h[n] == shft:
                    mod = "⇧"
                elif h[n] == fn:
                    mod = "Fn"
                else:
                    mod = "unknown"
                modString += mod
            return modString

    return "error"


if __name__ == "__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
