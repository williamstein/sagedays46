
import os

from sage.structure.sage_object import load, save
from sage.misc.all import tmp_filename

def _wait_in_thread(pid, callback, filename):
    def wait():    
        try:            
            os.waitpid(pid,0)            
            callback(load(filename))            
        except Exception, msg:
        	callback(msg)
                        
    from threading import Thread
    t = Thread(target=wait, args=tuple([]))
    t.start()
    
def async(f, args, kwds, callback):
    """
    Run f in a forked subprocess with given args and kwds, then call the 
    callback function when f terminates.
    """
    filename = tmp_filename() + '.sobj'
    sys.stdout.flush()
    sys.stderr.flush()
    pid = os.fork()
    if pid:
        # The parent master process
        try:
            _wait_in_thread(pid, callback, filename)        
            return pid
        finally:
            if os.path.exists(filename):
                os.unlink(filename)
    else:
        # The child process
        try:
            result = f(*args, **kwds)
        except Exception, msg:
            result = str(msg)
        save(result, filename)
        os._exit(0)


class Fork:
    """
    The %fork salvus decorator evaluates its code in a forked subprocess
    that does not block the main process.
            
    All (picklelable) global variables that are set in the forked subprocess are set in
    the parent when the forked subprocess terminates.  However, the forked subprocess
    has no other side effects, except what it might do to file handles and the filesystem.
            
    All pexpect interfaces are result in the child process. 
    """    
    def __init__(self):
        self._children = {}

    def children(self):
        return dict(self._children)
    
    def __call__(self, s):
        salvus._done = False
        
        id = salvus._id
        
        changed_vars = set([])
        
        def change(var, val):
            changed_vars.add(var)
        
        def f():
            # Run some commands to tell Sage that its
            # pid has changed.
            import sage.misc.misc
            reload(sage.misc.misc)
    
            # The pexpect interfaces (and objects defined in them) are
            # not valid.
            sage.interfaces.quit.invalidate_all()
    
            salvus.namespace.on('change', None, change)
            salvus.execute(s)
            result = {}
            for var in changed_vars:
                try:
                    result[var] = dumps(salvus.namespace[var])
                except:
                    result[var] = 'unable to pickle %s'%var
            return result
        
        def g(s):
            if isinstance(s, Exception):
                sys.stderr.write(s)
                sys.stderr.flush()
            else:
                for var, val in s.iteritems():
                    try:
                        salvus.namespace[var] = loads(val)
                    except:
                        print "unable to unpickle %s"%var                
            salvus._conn.send_json({'event':'output', 'id':id, 'done':True})   
            if pid in self._children:
                del self._children[pid]
            
        pid = async(f, tuple([]), {}, g)        
        print "Forked subprocess %s"%pid 
        self._children[pid] = id
        
    def kill(self, pid):
        if pid in self._children:
            salvus._conn.send_json({'event':'output', 'id':self._children[pid], 'done':True})
            os.kill(pid, 9)
            del self._children[pid]
        else:
            raise ValueError, "Unknown pid = (%s)"%pid
        
fork = Fork()        