from PyQt4 import QtCore, QtGui
from .. TreeWidget import TreeWidget
import collections, os, weakref, re
#import functions as fn

PARAM_TYPES = {}


def registerParameterType(name, cls, override=False):
    global PARAM_TYPES
    if name in PARAM_TYPES and not override:
        raise Exception("Parameter type '%s' already exists (use override=True to replace)" % name)
    PARAM_TYPES[name] = cls

class Parameter(QtCore.QObject):
    """Tree of name=value pairs (modifiable or not)
       - Value may be integer, float, string, bool, color, or list selection
       - Optionally, a custom widget may be specified for a property
       - Any number of extra columns may be added for other purposes
       - Any values may be reset to a default value
       - Parameters may be grouped / nested
       
    For more Parameter types, see ParameterTree.parameterTypes module.
    """
    ## name, type, limits, etc.
    ## can also carry UI hints (slider vs spinbox, etc.)
    
    sigValueChanged = QtCore.Signal(object, object)  ## self, value
    sigChildAdded = QtCore.Signal(object, object, object)  ## self, child, index
    sigChildRemoved = QtCore.Signal(object, object)  ## self, child
    sigParentChanged = QtCore.Signal(object, object)  ## self, parent
    sigLimitsChanged = QtCore.Signal(object, object)  ## self, limits
    sigNameChanged = QtCore.Signal(object, object)  ## self, name
    sigOptionsChanged = QtCore.Signal(object, object)  ## self, {opt:val, ...}
    
    ## Emitted when anything changes about this parameter at all.
    ## The second argument is a string indicating what changed ('value', 'childAdded', etc..)
    ## The third argument can be any extra information about the change
    sigStateChanged = QtCore.Signal(object, object, object) ## self, change, info
    
    ## emitted when any child in the tree changes state
    ## (but only if monitorChildren() is called)
    sigTreeStateChanged = QtCore.Signal(object, object, object, object)  # self, param, change, info
    
    
    def __new__(cls, *args, **opts):
        try:
            cls = PARAM_TYPES[opts['type']]
        except KeyError:
            pass
        #print "Build new:", cls
        return QtCore.QObject.__new__(cls, *args, **opts)
    
    def __init__(self, **opts):
        QtCore.QObject.__init__(self)
        
        self.opts = opts
        self.childs = []
        self.names = {}
        self.items = weakref.WeakKeyDictionary()
        self._parent = None
        
        if 'value' not in opts:
            opts['value'] = None
        
        if 'name' not in opts or not isinstance(opts['name'], basestring):
            raise Exception("Parameter must have a string name specified in opts.")
        
        for chOpts in opts.get('params', []):
            self.addChild(chOpts)
            
        if 'value' in opts and 'default' not in opts:
            opts['default'] = opts['value']
            
        ## Connect all state changed signals to the general sigStateChanged
        self.sigValueChanged.connect(lambda param, data: self.emitStateChanged('value', data))
        self.sigChildAdded.connect(lambda param, *data: self.emitStateChanged('childAdded', data))
        self.sigChildRemoved.connect(lambda param, data: self.emitStateChanged('childRemoved', data))
        self.sigParentChanged.connect(lambda param, data: self.emitStateChanged('parent', data))
        self.sigLimitsChanged.connect(lambda param, data: self.emitStateChanged('limits', data))
        self.sigNameChanged.connect(lambda param, data: self.emitStateChanged('name', data))
        self.sigOptionsChanged.connect(lambda param, data: self.emitStateChanged('options', data))
        
        
    def name(self):
        return self.opts['name']

    def setName(self, name):
        """Attempt to change the name of this parameter; return the actual name. 
        (The parameter may reject the name change or automatically pick a different name)"""
        parent = self.parent()
        if parent is not None:
            name = parent._renameChild(self, name)  ## first ask parent if it's ok to rename
        if self.opts['name'] != name:
            self.opts['name'] = name
            self.sigNameChanged.emit(self, name)
        return name

    def childPath(self, child):
        """Return the path of parameter names from self to child."""
        path = []
        while child is not self:
            path.insert(0, child.name())
            child = child.parent()
        return path

    def setValue(self, value, blockSignal=None):
        ## return the actual value that was set
        ## (this may be different from the value that was requested)
        #print self, "Set value:", value, self.opts['value'], self.opts['value'] == value
        try:
            if blockSignal is not None:
                self.sigValueChanged.disconnect(blockSignal)
            if self.opts['value'] == value:
                return value
            self.opts['value'] = value
            self.sigValueChanged.emit(self, value)
        finally:
            if blockSignal is not None:
                self.sigValueChanged.connect(blockSignal)
            
        return value

    def value(self):
        return self.opts['value']

    def getValues(self):
        """Return a tree of all values that are children of this parameter"""
        vals = collections.OrderedDict()
        for ch in self:
            vals[ch.name()] = (ch.value(), ch.getValues())
        return vals
    
    def saveState(self):
        """Return a structure representing the entire state of the parameter tree."""
        state = self.opts.copy()
        state['params'] = {ch.name(): ch.saveState() for ch in self}
        return state


    def defaultValue(self):
        return self.opts['default']
        
    def setDefault(self, val):
        self.opts['default'] = val

    def setToDefault(self):
        if self.hasDefault():
            self.setValue(self.defaultValue())

    def hasDefault(self):
        return 'default' in self.opts
        
    def valueIsDefault(self):
        return self.value() == self.defaultValue()
        
    def setLimits(self, limits):
        if 'limits' in self.opts and self.opts['limits'] == limits:
            return
        self.opts['limits'] = limits
        self.sigLimitsChanged.emit(self, limits)
        return limits

    def writable(self):
        return not self.opts.get('readonly', False)

    def setOpts(self, **opts):
        """For setting any arbitrary options."""
        changed = collections.OrderedDict()
        for k in opts:
            if k == 'value':
                self.setValue(opts[k])
            elif k == 'name':
                self.setName(opts[k])
            elif k == 'limits':
                self.setLimits(opts[k])
            elif k == 'default':
                self.setDefault(opts[k])
            elif k not in self.opts or self.opts[k] != opts[k]:
                self.opts[k] = opts[k]
                changed[k] = opts[k]
                
        if len(changed) > 0:
            self.sigOptionsChanged.emit(self, changed)
        
    def emitStateChanged(self, name, data):
        self.sigStateChanged.emit(self, name, data)


    def makeTreeItem(self, depth):
        """Return a TreeWidgetItem suitable for displaying/controlling the content of this parameter.
        Most subclasses will want to override this function.
        """
        if hasattr(self, 'itemClass'):
            #print "Param:", self, "Make item from itemClass:", self.itemClass
            return self.itemClass(self, depth)
        else:
            return ParameterItem(self, depth=depth)


    def addChild(self, child):
        """Add another parameter to the end of this parameter's child list."""
        return self.insertChild(len(self.childs), child)
        
    def insertChild(self, pos, child):
        """Insert a new child at pos.
        If pos is a Parameter, then insert at the position of that Parameter.
        If child is a dict, then a parameter is constructed as Parameter(**child)
        """
        if isinstance(child, dict):
            child = Parameter(**child)
        
        name = child.name()
        if name in self.names:
            if child.opts.get('autoIncrementName', False):
                name = self.incrementName(name)
                child.setName(name)
            else:
                raise Exception("Already have child named %s" % str(name))
        if isinstance(pos, Parameter):
            pos = self.childs.index(pos)
            
        if child.parent() is not None:
            child.remove()
            
        self.names[name] = child
        self.childs.insert(pos, child)
        
        child.parentChanged(self)
        self.sigChildAdded.emit(self, child, pos)
        
        return child
        
    def removeChild(self, child):
        name = child.name()
        if name not in self.names or self.names[name] is not child:
            raise Exception("Parameter %s is not my child; can't remove." % str(child))
        
        del self.names[name]
        self.childs.pop(self.childs.index(child))
        child.parentChanged(None)
        self.sigChildRemoved.emit(self, child)

    def parentChanged(self, parent):
        self._parent = parent
        self.sigParentChanged.emit(self, parent)
        
    def parent(self):
        return self._parent
        
    def remove(self):
        """Remove self from parent's child list"""
        parent = self.parent()
        if parent is None:
            raise Exception("Cannot remove; no parent.")
        parent.removeChild(self)

    def incrementName(self, name):
        ## return an unused name by adding a number to the name given
        base, num = re.match('(.*)(\d*)', name).groups()
        numLen = len(num)
        if numLen == 0:
            num = 2
            numLen = 1
        else:
            num = int(num)
        while True:
            newName = base + ("%%0%dd"%numLen) % num
            if newName not in self.childs:
                return newName
            num += 1

    def __iter__(self):
        for ch in self.childs:
            yield ch

    def __getitem__(self, *names):
        """Get the value of a child parameter"""
        return self.param(*names).value()

    def __setitem__(self, names, value):
        """Set the value of a child parameter"""
        if isinstance(names, basestring):
            names = (names,)
        return self.param(*names).setValue(value)

    def param(self, *names):
        """Return a child parameter. 
        Accepts the name of the child or a tuple (path, to, child)"""
        try:
            param = self.names[names[0]]
        except KeyError:
            raise Exception("Parameter %s has no child named %s" % (self.name(), names[0]))
        
        if len(names) > 1:
            return param.param(*names[1:])
        else:
            return param
        
    def __repr__(self):
        return "<%s '%s' at 0x%x>" % (self.__class__.__name__, self.name(), id(self))
       
    def __getattr__(self, attr):
        if attr in self.names:
            return self.param(attr)
        else:
            raise AttributeError(attr)
       
    def _renameChild(self, child, name):
        ## Only to be called from Parameter.rename
        if name in self.names:
            return child.name()
        self.names[name] = child
        del self.names[child.name()]
        return name

    def registerItem(self, item):
        self.items[item] = None
        
    def hide(self):
        self.show(False)
        
    def show(self, s=True):
        self.opts['visible'] = s
        self.sigOptionsChanged.emit(self, {'visible': s})


    def monitorChildren(self):
        self.watchParam(self)

    def watchParam(self, param):
        param.sigChildAdded.connect(self.grandchildAdded)
        param.sigChildRemoved.connect(self.grandchildRemoved)
        param.sigStateChanged.connect(self.grandchildChanged)
        for ch in param:
            self.watchParam(ch)

    def unwatchParam(self, param):
        param.sigChildAdded.disconnect(self.grandchildAdded)
        param.sigChildRemoved.disconnect(self.grandchildRemoved)
        param.sigStateChanged.disconnect(self.grandchildChanged)
        for ch in param:
            self.unwatchParam(ch)

    def grandchildAdded(self, parent, child):
        self.watchParam(child)
        
    def grandchildRemoved(self, parent, child):
        self.unwatchParam(child)
        
    def grandchildChanged(self, param, change, data):
        self.sigTreeStateChanged.emit(self, param, change, data)
        
            

class ParameterTree(TreeWidget):
    """Widget used to display or control data from a ParameterSet"""
    
    def __init__(self, parent=None):
        TreeWidget.__init__(self, parent)
        self.setAnimated(False)
        self.setColumnCount(2)
        self.setHeaderLabels(["Parameter", "Value"])
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.paramSet = None
        self.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.itemChanged.connect(self.itemChangedEvent)
        self.lastSel = None
        self.setRootIsDecorated(False)
        
    def setParameters(self, param, root=None, depth=0, showTop=True):
        item = param.makeTreeItem(depth=depth)
        if root is None:
            root = self.invisibleRootItem()
            ## Hide top-level item
            if not showTop:
                item.setSizeHint(0, QtCore.QSize(0,0))
                item.setSizeHint(1, QtCore.QSize(0,0))
                depth -= 1
        root.addChild(item)
        item.treeChanged()
            
        #expand = False
        for ch in param:
            #item = param.makeTreeItem(depth=depth)
            #root.addChild(item)
            #item.treeChanged()
            self.setParameters(ch, root=item, depth=depth+1)
            #expand = True
        #root.setExpanded(expand)
        
        #self.paramSet = param
        
    #def resizeEvent(self):
        #for col in range(self.columnCount()):
            #if self.columnWidth(col) < self.sizeHintForColumn(col):
                #self.resizeColumnToContents(0)

    def contextMenuEvent(self, ev):
        item = self.currentItem()
        if hasattr(item, 'contextMenuEvent'):
            item.contextMenuEvent(ev)
            
    def itemChangedEvent(self, item, col):
        if hasattr(item, 'columnChangedEvent'):
            item.columnChangedEvent(col)
            
    def selectionChanged(self, *args):
        sel = self.selectedItems()
        if len(sel) != 1:
            sel = None
        if self.lastSel is not None:
            self.lastSel.selected(False)
        if sel is None:
            self.lastSel = None
            return
        self.lastSel = sel[0]
        if hasattr(sel[0], 'selected'):
            sel[0].selected(True)
        return TreeWidget.selectionChanged(self, *args)
        


class ParameterItem(QtGui.QTreeWidgetItem):
    """
    Abstract ParameterTree item. 
        - Sets first column of item to name
        - generates context menu if item is renamable or removable
        - handles child added / removed events
        - provides virtual functions for handling changes from parameter
    For more ParameterItem types, see ParameterTree.parameterTypes module.
    """
    
    def __init__(self, param, depth=0):
        QtGui.QTreeWidgetItem.__init__(self, [param.name(), ''])
        
        self.param = param
        self.param.registerItem(self)  ## let parameter know this item is connected to it (for debugging)
        self.depth = depth
        
        param.sigValueChanged.connect(self.valueChanged)
        param.sigChildAdded.connect(self.childAdded)
        param.sigChildRemoved.connect(self.childRemoved)
        param.sigNameChanged.connect(self.nameChanged)
        param.sigLimitsChanged.connect(self.limitsChanged)
        param.sigOptionsChanged.connect(self.optsChanged)
        
        opts = param.opts
        
        ## Generate context menu for renaming/removing parameter
        self.contextMenu = QtGui.QMenu()
        self.contextMenu.addSeparator()
        flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if opts.get('renamable', False):
            flags |= QtCore.Qt.ItemIsEditable
            self.contextMenu.addAction('Rename').triggered.connect(self.editName)
        if opts.get('removable', False):
            self.contextMenu.addAction("Remove").triggered.connect(self.param.remove)
        
        ## handle movable / dropEnabled options
        if opts.get('movable', False):
            flags |= QtCore.Qt.ItemIsDragEnabled
        if opts.get('dropEnabled', False):
            flags |= QtCore.Qt.ItemIsDropEnabled
        self.setFlags(flags)
        
        ## flag used internally during name editing
        self.ignoreNameColumnChange = False
    
    
    def valueChanged(self, param, val):
        ## called when the parameter's value has changed
        pass
    
    def treeChanged(self):
        """Called when this item is added or removed from a tree.
        Expansion, visibility, and column widgets must all be configured AFTER 
        the item is added to a tree, not during __init__.
        """
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))
        
    def childAdded(self, param, child, pos):
        item = child.makeTreeItem(depth=self.depth+1)
        self.insertChild(pos, item)
        item.treeChanged()
        
        for i, ch in enumerate(child):
            item.childAdded(child, ch, i)
        
    def childRemoved(self, param, child):
        for i in range(self.childCount()):
            item = self.child(i)
            if item.param is child:
                self.takeChild(i)
                break
                
    def contextMenuEvent(self, ev):
        if not self.param.opts.get('removable', False) and not self.param.opts.get('renamable', False):
            return
            
        self.contextMenu.popup(ev.globalPos())
        
    def columnChangedEvent(self, col):
        """Called when the text in a column has been edited.
        By default, we only use changes to column 0 to rename the parameter.
        """
        if col == 0:
            if self.ignoreNameColumnChange:
                return
            newName = self.param.setName(str(self.text(col)))
            try:
                self.ignoreNameColumnChange = True
                self.nameChanged(self, newName)  ## If the parameter rejects the name change, we need to set it back.
            finally:
                self.ignoreNameColumnChange = False
                
    def nameChanged(self, param, name):
        ## called when the parameter's name has changed.
        self.setText(0, name)

    def limitsChanged(self, param, limits):
        """Called when the parameter's limits have changed"""
        pass

    def optsChanged(self, param, opts):
        """Called when any options are changed that are not
        name, value, default, or limits"""
        #print opts
        if 'visible' in opts:
            self.setHidden(not opts['visible'])
        
    def editName(self):
        self.treeWidget().editItem(self, 0)
        
    def selected(self, sel):
        """Called when this item has been selected (sel=True) OR deselected (sel=False)"""
        pass


