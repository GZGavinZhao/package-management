# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, Solus Project
# SPDX-License-Identifier: GPL-2.0-or-later

"""
 xmlext is a helper module for accessing XML files using
 xml.dom.minidom . It is a convenient wrapper for some
 DOM functions, and provides path based get/add functions
 as in KDE API.

 function names are mixedCase for compatibility with minidom,
 an 'old library'

 this implementation uses piksemel
"""

from pisi import translate as _

import pisi
import iksemel as iks

parse = iks.parse
newDocument = iks.newDocument


def getAllNodes(node, tagPath):
    """retrieve all nodes that match a given tag path."""
    tags = tagPath.split("/")
    if len(tags) == 0:
        return []
    nodeList = [node]  # basis case
    for tag in tags:
        results = [getTagByName(x, tag) for x in nodeList]
        nodeList = []
        for x in results:
            nodeList.extend(x)
            pass  # emacs indentation error, keep it here
        if len(nodeList) == 0:
            return []
    return nodeList


def getNodeAttribute(node, attrname):
    """get named attribute from DOM node"""
    return node.getAttribute(attrname)


def setNodeAttribute(node, attrname, value):
    """get named attribute from DOM node"""
    return node.setAttribute(attrname, value)


def getChildElts(parent):
    """get only child elements"""
    return [x for x in parent.tags()]


def getTagByName(parent, childName):
    return [x for x in parent.tags(childName)]


def getNodeText(node, tagpath=""):
    """get the first child and expect it to be text!"""
    if tagpath != "":
        node = getNode(node, tagpath)
        if not node:
            return None
    child = node.firstChild()
    if not child:
        return None
    if child.type() == iks.DATA:
        # in any case, strip whitespaces...
        return child.data().strip()
    else:
        raise iks.XmlError(_("getNodeText: Expected text node, got something else!"))


def getChildText(node_s, tagpath):
    """get the text of a child at the end of a tag path"""
    node = getNode(node_s, tagpath)
    if not node:
        return None
    return getNodeText(node)


def getNode(node, tagpath):
    """returns the *first* matching node for given tag path."""

    if tagpath == "":
        return node

    assert type(tagpath) == str
    tags = tagpath.split("/")
    assert len(tags) > 0

    # iterative code to search for the path
    for tag in tags:
        currentNode = None
        for child in node.tags():
            if child.name() == tag:
                currentNode = child
                break
        if not currentNode:
            return None
        else:
            node = currentNode
    return currentNode


def createTagPath(node, tags):
    """create new child at the end of a tag chain starting from node
    no matter what"""
    if len(tags) == 0:
        return node
    for tag in tags:
        node = node.insertTag(tag)
    return node


def addTagPath(node, tags, newnode=None):
    """add newnode at the end of a tag chain, smart one"""
    node = createTagPath(node, tags)
    if newnode:  # node to add specified
        node.insertNode(newnode)
    return node


def addNode(node, tagpath, newnode=None, branch=True):
    """add a new node at the end of the tree and returns it
    if newnode is given adds that node, too."""

    assert type(tagpath) == str
    tags = []
    if tagpath != "":
        tags = tagpath.split("/")  # tag chain
    else:
        addTagPath(node, [], newnode)
        return node  # FIXME: is this correct!?!?

    assert len(tags) > 0  # we want a chain

    # iterative code to search for the path

    if branch:
        rem = 1
    else:
        rem = 0

    while len(tags) > rem:
        tag = tags.pop(0)
        nodeList = getTagByName(node, tag)
        if len(nodeList) == 0:  # couldn't find
            tags.insert(0, tag)  # put it back in
            return addTagPath(node, tags, newnode)
        else:
            node = nodeList[len(nodeList) - 1]  # discard other matches
    else:
        # had only one tag..
        return addTagPath(node, tags, newnode)

    return node


def addText(node, tagpath, text):
    node = addNode(node, tagpath)
    node.insertData(text)


def newNode(node, tag):
    return iks.newDocument(tag)
