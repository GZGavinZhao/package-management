# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, 2017-Present Solus Developers
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

import xml.etree.ElementTree as xml
from typing import Iterable, Iterator

from pisi import translate as _


def getAllNodes(node: xml.Element, tagPath: str) -> list[xml.Element]:
    """retrieve all nodes that match a given tag path."""
    tags = tagPath.split("/")
    if len(tags) == 0:
        return []
    nodeList = [node]  # basis case
    for tag in tags:
        nodeList = []
        for x in (getTagByName(x, tag) for x in nodeList):
            nodeList.extend(x)
        if len(nodeList) == 0:
            return []
    return nodeList


def getNodeAttribute(node: xml.Element, attrname: str) -> str | None:
    """get named attribute from DOM node"""
    return node.attrib.get(attrname)


def setNodeAttribute(node: xml.Element, attrname: str, value: str):
    """set named attribute from DOM node"""
    node.attrib[attrname] = value


def getChildElts(parent: xml.Element) -> Iterator[xml.Element]:
    """get only child elements"""
    return iter(parent)


def getTagByName(parent: xml.Element, childName: str) -> Iterator[xml.Element]:
    return parent.iterfind(childName)


def getNodeText(node: xml.Element, tagpath: str) -> str | None:
    """get the first child and expect it to be text!"""
    if node.tag == tagpath:
        return node.text
    child = getNode(node, tagpath)
    if child is None:
        return None
    return child.text


def getNode(node: xml.Element, tagpath: str) -> xml.Element | None:
    """
    returns the *first* matching node for given tag path.
    tagpath is an XPath.
    """
    return node.find(tagpath)


def createTagPath(node: xml.Element, tags: Iterable[str]):
    """create new child at the end of a tag chain starting from node
    no matter what"""
    for tag in tags:
        node = xml.SubElement(node, tag)
    return node


def addTagPath(
    node: xml.Element, tags: Iterable[str], newnode: xml.Element | None = None
):
    """add newnode at the end of a tag chain, smart one"""
    node = createTagPath(node, tags)
    if newnode:  # node to add specified
        node.append(newnode)
    return node


def addNode(
    node: xml.Element, tagpath: str, newnode: xml.Element | None = None
) -> xml.Element:
    """add a new node at the end of the tree and returns it
    if newnode is given adds that node, too."""

    if tagpath == "":
        if newnode is not None:
            node.append(newnode)
            node = newnode
        return node
    for tag in tagpath.split("/"):
        child = node.find(tag)
        if child is None:
            child = xml.Element(tag)
            node.append(child)
        node = child
    if newnode is not None:
        node.append(newnode)
        node = newnode
    return node


def addText(node: xml.Element, tagpath: str, text: str):
    node = addNode(node, tagpath)
    node.text = text


def newNode(tag: str) -> xml.Element:
    return xml.Element(tag)
