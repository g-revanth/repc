from status import Status
from lock_type import LockType
from collections import defaultdict
from variable import Variable
from lock import Lock
class Site:
    def __init__(self,name, status, vars):
        self.name = name
        self.status = status
        self.variables = vars #dict of var name and var obj
        self.lock_table = defaultdict(list) # dict of var name and list of locks

    def can_acquire_read_lock(self, t_id, var_name):
        for lock in self.lock_table[var_name]:
            if lock.lock_type == lock_type.WRITE and lock.t_id != t_id:
                print("Cannot Acquire Lock and Write Lock Already acquired by another t_id")
                return False
        return True

    def acquire_read_lock(self, t_id, var_name):
        for lock in self.lock_table[var_name]:
            if lock.t_id == t_id:
                print('Lock Already exist')
                return
        print('Lock doesnt exist, create a new read lock')
        self.lock_table[var_name].append(Lock(LockType.READ, var_name, t_id))

    def can_acquire_write_lock(self, t_id, var_name):
        for lock in self.lock_table[var_name]:
            if lock.lock_type != lock_type.NO_LOCK and lock.t_id != t_id:
                print("Cannot Acquire Write Lock as Lock Already acquired by another t_id")
                return False
        return True

    def acquire_write_lock(self, t_id, var_name):
        found = False
        curr_lock = None
        for lock in self.lock_table[var_name]:
            if lock.t_id == t_id:
                print('Lock Already exist')
                curr_lock = lock
                found = True
                break
        if not found:
            print('Lock doesnt exist, create a new read lock')
            self.lock_table[var_name].append(Lock(LockType.WRITE, var_name, t_id))
        else:
            curr_lock.lock_type = LockType.WRITE # promote lock to write lock


    def release_locks(self,t_id, var_name):
        cpy_list = []
        for lock in self.lock_table[var_name]:
            if lock.t_id != t_id:
                cpy_list.append(lock)
        self.lock_table[var_name] = cpy_list

    def fail(self):
        self.status = Status.FAILED
        self.lock_table.clear()
    
    def recover(self):
        pass
    
    def can_read(self, t_id, var_name):
        if not self.status.AVAILABLE:
            return False
        if var_name not in self.variables:
            return False
        return self.can_acquire_read_lock(t_id, var_name)
        

class SiteManager:
    def __init__(self):
        num_site = 10
        num_var = 20
        sites = defaultdict(Site)
        for i in range(1, num_site+1):
            variables = defaultdict(Variable)
            for j in range(1, num_var+1):
                if j % 2 == 0 or (j % 2 != 0 and (1+ j%10) == i):
                    var = Variable('x'+str(j), 10*j, Lock(LockType.NO_LOCK, 'x'+str(j)))
                    variables['x'+str(j)] = var             
            s = Site(str(i),Status.READY, variables)
            sites[str(i)] = s        
        self.sites = sites

    def read(self, t_id, var):
        for name, site in self.sites.items():
            if site.can_read(t_id, var):
                site.acquire_read_lock(t_id, var)
                return (site.variables[var].val, site.name)
        
        
    def write(self, transaction, var, val):
        pass

    def end(self, transaction):
        pass