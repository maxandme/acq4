# -*- coding: utf-8 -*-
from lib.drivers.MultiClamp import MultiClamp as MultiClampDriver
from lib.devices.Device import *
from lib.util.MetaArray import MetaArray, axis
from numpy import *

class MultiClamp(Device):
    def __init__(self, dm, config, name):
        self.dm = dm
        self.config = config.copy()
        self.name = name
        if not config.has_key('host') or config['host'] is None:
            raise Exception("Must specify host running MultiClamp server. (Direct connections not yet supported..)")
        self.host = self.config['host']
        if ':' in self.host:
            (host, c, port) = self.host.partition(':')
            args = (host, port)
        else:
            args = (self.host,)
        self.mc = MultiClampDriver(*args)
        
        try:
            mcs = self.mc.listDevices()
            print "Connected to host %s, devices are %s" % (self.host, repr(mcs))
            self.channelID = self.config['channelID']
            self.index = None ## Avoid probing the MC devices until later on
        except:
            print "Error connecting to MultiClamp commander, will try again when needed."
        
        print "Created MultiClamp device"
    
    def createTask(self, cmd):
        return Task(self, cmd)
    
        
    def setHolding(self, mode=None):
        """Set all channel for this device to its configured holding level. If mode is None, then
        the level is chosen based on the current mode of the channel."""
        chan = self.getChanIndex()

        if mode is None:
            mode = self.mc.runFunction('getMode', [chan])[0]
    
        ### Set correct holding level here...
        
        
    def getChanIndex(self):
        """Given a channel name (as defined in the configuration), return the device index to use when making calls to the MC"""
        if self.index is None:
            devs = self.mc.listDevices()
            if self.channelID not in devs:
                raise Exception("Could not find device on multiclamp with description '%s'" % self.channelID)
            self.index = devs.index(self.channelID)
        return self.index
        

    def devRackInterface(self):
        """Return a widget with a UI to put in the device rack"""
        pass
        
    def protocolInterface(self):
        """Return a widget with a UI to put in the protocol rack"""
        pass

    def setMode(self, mode):
        """Set the mode for a multiclamp channel, gracefully switching between VC and IC modes."""

        if mode not in ['VC', 'IC', 'I=0']:
            raise Exception('MultiClamp mode "%s" not recognized.' % mode)
        
        chan = self.getChanIndex()

        mcMode = self.mc.runFunction('getMode', [chan])[0]
        
        ## If switching ic <-> vc, switch to i=0 first
        if (mcMode=='IC' and mode=='VC') or (mcMode=='VC' and mode=='IC'):
            self.mc.runFunction('setMode', [chan,'I=0'])
            mcMode = 'I=0'
        
        if mcMode=='I=0':
            ## Set holding level before leaving I=0 mode
            self.setHolding(mode=mode)
        
        self.mc.runFunction('setMode', [chan, mode])

    def quit(self):
        self.mc.disconnect()

class Task(DeviceTask):
    def __init__(self, dev, cmd):
        self.dev = dev
        self.cmd = cmd
        self.recordParams = ['Holding', 'HoldingEnable', 'PipetteOffset', 'FastCompCap', 'SlowCompCap', 'FastCompTau', 'SlowCompTau', 'NeutralizationEnable', 'NeutralizationCap', 'WholeCellCompEnable', 'WholeCellCompCap', 'WholeCellCompResist', 'RsCompEnable', 'RsCompBandwidth', 'RsCompCorrection', 'PrimarySignalGain', 'PrimarySignalLPF', 'PrimarySignalHPF', 'OutputZeroEnable', 'OutputZeroAmplitude', 'LeakSubEnable', 'LeakSubResist', 'BridgeBalEnable', 'BridgeBalResist']
        self.usedChannels = None
        self.daqTasks = {}
        
    def configure(self, tasks, startOrder):
        ## set MC state, record state
        """Sets the state of a remote multiclamp to prepare for a program run."""
            
        ch = self.dev.getChanIndex()
        
        ## Set state of clamp
        self.dev.setMode(self.cmd['mode'])
        if 'scaled' in self.cmd:
            self.dev.mc.setPrimarySignalByName(ch, self.cmd['scaled'])
        if 'raw' in self.cmd:
            self.dev.mc.setSecondarySignalByName(ch, self.cmd['raw'])
        
        if self.cmd.has_key('parameters'):
            for k in self.cmd['parameters']:
                self.dev.mc.setParameter(ch, k, self.cmd['parameters'][k])
        
        self.state = {}
        if self.cmd.has_key('recordState') and self.cmd['recordState']:
            self.state = self.dev.mc.readParams(ch, self.recordParams)
            
        self.state['scaledSignal'] = self.dev.mc.getSignalInfo(ch, 'Primary')
        self.state['rawSignal'] = self.dev.mc.getSignalInfo(ch, 'Secondary')
        
                
    def getUsedChannels(self):
        """Return a list of the channels this task uses"""
        if self.usedChannels is None:
            self.usedChannels = []
            for ch in ['scaled', 'raw', 'command']:
                if ch in self.cmd:
                    self.usedChannels.append(ch)
                    
        return self.usedChannels
        
                
    def createChannels(self, daqTask):
        ## Is this the correct DAQ device for any of my channels?
        ## create needed channels + info
        ## write waveform to command channel if needed
        
        for ch in self.getUsedChannels():
            chConf = self.dev.config[ch+'Channel']
            if chConf[0] == daqTask.devName():
                if ch == 'command':
                    daqTask.addChannel(chConf[1], 'ao')
                    scale = self.dev.config['cmdScale'][self.cmd['mode']]
                    cmdData = self.cmd['command'] * scale
                    daqTask.setWaveform(chConf[1], cmdData)
                else:
                    daqTask.addChannel(chConf[1], 'ai')
                self.daqTasks[ch] = daqTask
        
    def start(self):
        ## possibly nothing required here, DAQ will start recording.
        pass
        
    def isDone(self):
        ## DAQ task handles this for us.
        return True
        
    def getResult(self):
        ## Access data recorded from DAQ task
        ## create MetaArray and fill with MC state info
        #self.state['startTime'] = self.daqTasks[self.daqTasks.keys()[0]].getStartTime()
        
        result = {}
        #result['info'] = self.state
        for ch in self.usedChannels:
            chConf = self.dev.config[ch+'Channel']
            result[ch] = self.daqTasks[ch].getData(chConf[1])
            # print result[ch]
            if ch == 'command':
                result[ch]['data'] = result[ch]['data'] / self.dev.config['cmdScale'][self.cmd['mode']]
                result[ch]['name'] = 'Command'
                if self.cmd['mode'] == 'VC':
                    result[ch]['units'] = 'V'
                else:
                    result[ch]['units'] = 'A'
            else:
                scale = 1.0 / self.state[ch + 'Signal'][1]
                result[ch]['data'] = result[ch]['data'] * scale
                result[ch]['units'] = self.state[ch + 'Signal'][2]
                result[ch]['name'] = self.state[ch + 'Signal'][0]
            
        # print result
            
        ## Copy state from first channel (assume this is the same for all channels)
        firstChInfo = result[self.usedChannels[0]]['info']
        for k in firstChInfo:
            self.state[k] = firstChInfo[k]
            
        timeVals = linspace(0, float(self.state['numPts']-1) / float(self.state['rate']), self.state['numPts'])
        chanList = [atleast_2d(result[x]['data']) for x in result]
        # for l in chanList:
          # print l.shape
        cols = [(result[x]['name'], result[x]['units']) for x in result]
        # print cols
        arr = concatenate(chanList)
        info = [axis(name='Channel', cols=cols), axis(name='Time', units='s', values=timeVals)] + [self.state]
        marr = MetaArray(arr, info=info)
            
        return marr